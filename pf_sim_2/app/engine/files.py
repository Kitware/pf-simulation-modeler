import logging
import time
import os
import yaml
import random
from trame.app.singleton import Singleton


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@Singleton
class FileDatabase:
    def __init__(self):
        self._datastore = None
        self.entries = {}

    @property
    def datastore(self) -> str:
        if self._datastore is None:
            raise Exception("Using FileDatabase before initializing its datastore")

        return self._datastore

    @datastore.setter
    def datastore(self, ds):
        self._datastore = ds
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
        try:
            with open(path) as entriesFile:
                return yaml.safe_load(entriesFile) or {}
        except FileNotFoundError:
            return {}

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


class FileLogic:
    def __init__(self, state, ctrl, args):
        self.state = state
        self.ctrl = ctrl

        file_database = FileDatabase()
        file_database.datastore = args["datastore"]
        entries = file_database.getEntries()

        state.update(
            {
                **args,
                "file_categories": [
                    "Indicator",
                    "Elevation",
                    "Slope",
                    "Pressure",
                    "Other",
                ],
                "upload_error": "",
                "db_files": entries,
                "db_selected_file": None if not entries else list(entries.values())[0],
            }
        )

        ctrl.trigger("uploadFile")(self.uploadFile)
        ctrl.trigger("uploadLocalFile")(self.uploadLocalFile)
        ctrl.trigger("updateFile")(self.updateFile)

    def uploadFile(self, entryId, fileObj):
        if not fileObj or not entryId:
            logger.info("No file or entryId provided")
            return

        file_database = FileDatabase()

        try:
            updateEntry = {
                "origin": fileObj["name"],
                "size": fileObj["size"],
                "type": fileObj["type"],
                "dateModified": fileObj["lastModified"],
                "dateUploaded": int(time.time() * 1000),
            }
            file_database.writeEntryData(entryId, fileObj["content"])
        except Exception as e:
            logger.error(f">>> Error uploading file: {e}")
            self.state.upload_error = (
                "An error occurred uploading the file to the database."
            )
            return

        entry = {**file_database.getEntry(entryId), **updateEntry}
        file_database.writeEntry(entryId, entry)
        self.state.db_selected_file = entry

    def uploadLocalFile(self, entryId, fileMeta):
        sharedir = self.state.sharedir

        if sharedir is None:
            return

        file_database = FileDatabase()

        updateEntry = {
            key: fileMeta.get(key)
            for key in ["origin", "size", "dateModified", "dateUploaded", "type"]
        }

        try:
            updateEntry = {
                "type": fileMeta["type"],
                "dateModified": int(time.time()),
                "dateUploaded": int(time.time()),
            }

            file_path = os.path.abspath(os.path.join(sharedir, fileMeta["localFile"]))
            if os.path.commonpath([sharedir, file_path]) != sharedir:
                raise Exception("Attempting to access a file outside the sharedir.")
            updateEntry["origin"] = os.path.basename(file_path)

            with open(file_path, "rb") as f:
                content = f.read()
                updateEntry["size"] = len(content)
                file_database.writeEntryData(entryId, content)
        except Exception as e:
            print(e)
            self.state.upload_error = (
                "An error occurred uploading the file to the database."
            )
            return

        entry = {**file_database.getEntry(entryId), **updateEntry}
        file_database.writeEntry(entryId, entry)
        self.state.db_selected_file = entry

    def updateFile(self, update, entryId=None):
        file_database = FileDatabase()

        if update == "selectFile":
            if self.state.db_files.get(entryId):
                self.state.db_selected_file = file_database.getEntry(entryId)
            else:
                self.state.db_selected_file = None

        elif update == "removeFile":
            file_database.deleteEntry(entryId)
            self.state.db_files = file_database.getEntries()
            if (
                self.state.db_selected_file
                and entryId == self.state.db_selected_file.get("id")
            ):
                self.state.db_selected_file = None

        elif update == "downloadSelectedFile":
            self.state.dbFileExchange = file_database.getEntryData(entryId)

        self.state.upload_error = ""


def initialize(server, args):
    state, ctrl = server.state, server.controller

    FileLogic(state, ctrl, args)

    @state.change("db_selected_file")
    def changeCurrentFile(db_selected_file, **kwargs):
        if db_selected_file is None:
            return

        file_database = FileDatabase()
        file_id = db_selected_file.get("id")

        if not file_id:
            db_selected_file = file_database.addNewEntry(db_selected_file)
            db_selected_file = None
        else:
            current_entry = file_database.getEntry(file_id)
            db_selected_file = {**current_entry, **db_selected_file}
            file_database.writeEntry(file_id, db_selected_file)

        state.db_selected_file = db_selected_file
        state.db_files = file_database.getEntries()
