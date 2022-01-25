import os
import random
import yaml
from typing import Optional
from enum import Enum

from trame import state, trigger
from parflowio.pyParflowio import PFData


class FileCategories(str, Enum):
    Indicator = "INDICATOR"
    Terrain = "TERRAIN"
    Other = "OTHER"


def file_category_label(category: FileCategories) -> str:
    if category is FileCategories.Indicator:
        return "Indicator"
    elif category is FileCategories.Terrain:
        return "Terrain"
    elif category is FileCategories.Other:
        return "Other"
    else:
        raise Exception(f"Unknown file category: {category}")


class FileDatabase:
    def __init__(self, datastore):
        self.datastore = datastore
        self.entries = self._loadEntries()

    def addNewEntry(self, newFile):
        entryId = str(random.getrandbits(32))
        dataId = str(random.getrandbits(32))
        newFile["id"] = entryId
        newFile["dataId"] = dataId
        self.writeEntry(entryId, newFile)
        return newFile

    def writeEntry(self, entryId, metadata):
        self.entries = {**self.entries, entryId: metadata}
        self._writeEntries(self.entries)

    def _writeEntries(self, entries):
        path = self._getDbPath()
        with open(path, "w") as db:
            yaml.dump(entries, db)

    def _loadEntries(self):
        path = self._getDbPath()
        with open(path) as entriesFile:
            return yaml.safe_load(entriesFile) or {}

    def _getDbPath(self):
        return os.path.join(self.datastore, "pf_datastore.yaml")

    def getEntry(self, entryId):
        return self.entries.get(entryId)

    def getEntries(self):
        return self.entries

    def getEntryPath(self, entryId):
        if entryId is None:
            raise Exception("Failed to find path for empty entryId")
        entry = self.entries[entryId]
        dataId = entry.get("dataId")

        if dataId is None:
            raise Exception(
                f"Could not find dataId for entry {entryId} while finding path"
            )

        return os.path.join(self.datastore, dataId)

    def getEntryData(self, entryId):
        path = self.getEntryPath(entryId)
        with open(path, "rb") as entryFile:
            return entryFile.read()

    def writeEntryData(self, entryId, content):
        path = self.getEntryPath(entryId)

        with open(path, "wb") as entryFile:
            entryFile.write(content)

    def deleteEntry(self, entryId):
        path = self.getEntryPath(entryId)

        entries = {**self.entries}
        del entries[entryId]
        self.entries = entries
        self._writeEntries(self.entries)

        try:
            os.remove(path)
        except FileNotFoundError:
            print("The underlying file did not exist.")


def file_changes(file_database):
    @state.change("dbSelectedFile")
    def changeCurrentFile(dbSelectedFile, dbFiles, **kwargs):
        if dbSelectedFile is None:
            return

        file_id = dbSelectedFile.get("id")

        if not file_id:
            dbSelectedFile = file_database.addNewEntry(dbSelectedFile)
        else:
            currentEntry = file_database.getEntry(file_id)
            dbSelectedFile = {**currentEntry, **dbSelectedFile}
            file_database.writeEntry(file_id, dbSelectedFile)

        state.dbSelectedFile = dbSelectedFile
        state.flush("dbSelectedFile")
        state.dbFiles = file_database.getEntries()

    @state.change("indicatorFile")
    def updateComputationalGrid(indicatorFile, **kwargs):
        entry = file_database.getEntry(indicatorFile)
        state.indicatorFileDescription = entry.get("description")

        filename = file_database.getEntryPath(indicatorFile)
        try:
            handle = PFData(filename)
        except:
            print(f"Could not find pfb: {filename}")
            return
        handle.loadHeader()

        state.NX = handle.getNX()
        state.NY = handle.getNY()
        state.NZ = handle.getNZ()

        state.LX = handle.getX()
        state.LY = handle.getY()
        state.LZ = handle.getZ()

        state.DX = handle.getDX()
        state.DY = handle.getDY()
        state.DZ = handle.getDZ()

    @state.change("dbFileExchange")
    def saveUploadedFile(
        dbFileExchange=None, dbSelectedFile=None, sharedir=None, **kwargs
    ):
        if dbFileExchange is None or dbSelectedFile is None or sharedir is None:
            return

        fileMeta = {
            key: dbFileExchange.get(key)
            for key in ["origin", "size", "dateModified", "dateUploaded", "type"]
        }
        entryId = dbSelectedFile.get("id")

        try:
            # File was uploaded from the user browser
            if dbFileExchange.get("content"):
                file_database.writeEntryData(entryId, dbFileExchange["content"])
            # Path to file already present on the server was specified
            elif dbFileExchange.get("localFile"):
                file_path = os.path.abspath(
                    os.path.join(sharedir, dbFileExchange.get("localFile"))
                )
                if os.path.commonpath([sharedir, file_path]) != sharedir:
                    raise Exception("Attempting to access a file outside the sharedir.")
                fileMeta["origin"] = os.path.basename(file_path)

                with open(file_path, "rb") as f:
                    content = f.read()
                    fileMeta["size"] = len(content)
                    file_database.writeEntryData(entryId, content)
        except Exception as e:
            print(e)
            state.uploadError = "An error occurred uploading the file to the database."
            return

        entry = {**file_database.getEntry(entryId), **fileMeta}
        file_database.writeEntry(entryId, entry)
        state.dbSelectedFile = entry
        state.flush("dbSelectedFile")

    @trigger("updateFiles")
    def updateFiles(update, entryId=None):
        if update == "selectFile":
            if state.dbFiles.get(entryId):
                state.dbSelectedFile = file_database.getEntry(entryId)

        elif update == "removeFile":
            file_database.deleteEntry(entryId)
            state.dbFiles = file_database.getEntries()
            if entryId == state.dbSelectedFile.get("id"):
                state.dbSelectedFile = None
                state.flush("dbSelectedFile")
            state.flush("dbFiles")

        elif update == "downloadSelectedFile":
            state.dbFileExchange = file_database.getEntryData(entryId)

        state.uploadError = ""
