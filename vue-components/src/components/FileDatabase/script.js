import DragAndDropFiles from '../DragAndDropFiles';

export default {
  name: 'FileDatabase',
  components: {
    DragAndDropFiles,
  },
  props: ['files', 'fileCategories', 'value', 'error'],
  data() {
    return {
      searchQuery: '',
      fileStats: {},
      file: null,
      formContent: this.value || {},
    };
  },
  methods: {
    iconFromType(type) {
      if (type === 'zip') return 'mdi-folder-zip';
      if (type === 'folder') return 'mdi-folder';
      return 'mdi-file';
    },
    searchMatch(file) {
      if (this.searchQuery === '') return true;
      const regex = new RegExp(this.searchQuery);
      const checks = [file.name, file.description, file.category, file.type];
      for (var i = 0; i < checks.length; i++) {
        if (checks[i] && checks[i].search(regex) > -1) return true;
      }
      return false;
    },
    uploaded(file) {
      if (file) {
        this.fileStats = {
          size: file.size,
          origin: file.name,
          dateModified: file.lastModified,
          dateUploaded: Number(new Date()),
          type: file.type === 'application/zip' ? 'zip' : 'file',
        };
      } else {
        this.fileStats = {};
      }
      this.file = file;
    },
    selectFile(id) {
      this.trame.trigger('updateFile', ['selectFile', id]);
    },
    removeFile(id) {
      this.trame.trigger('updateFile', ['removeFile', id]);
    },
    downloadSelectedFile() {
      this.trame.trigger('updateFile', ['downloadSelectedFile', this.value.id]);
    },
    resetSelectedFile() {
      this.file = null;
      this.fileStats = {};
    },
    newFile() {
      this.fileStats = {};
      let name = 'unnamed file';
      let count = 1;
      const fileList = Object.values(this.files);
      while (fileList.find((file) => file.name === name + ' ' + count)) {
        count++;
      }
      name = name + ' ' + count;
      this.$emit('input', {
        name,
        description: '',
        origin: null,
        size: null,
        dateModified: null,
        dateUploaded: null,
        type: null,
        gridSize: null,
        category: null,
      });
    },
    save() {
      /*eslint no-unused-vars: ["error", { "ignoreRestSiblings": true }]*/
      const {
        useLocalFile,
        copyLocalFile,
        localFile,
        origin,
        dateModified,
        dateUploaded,
        type,
        size,
        ...formContent
      } = this.formContent;
      if (!useLocalFile && this.file) {
        this.trame.trigger('uploadFile', [this.value.id, this.file]);
        this.resetSelectedFile();
      } else if (useLocalFile && localFile) {
        const fileMeta = {
          copyLocalFile,
          localFile,
          type: 'file',
        };
        this.trame.trigger('uploadLocalFile', [this.value.id, fileMeta]);
      }

      this.$emit('input', { ...formContent });
    },
    cancel() {
      this.formContent = { ...(this.value || {}) };
      this.resetSelectedFile();
    },
  },
  computed: {
    origin() {
      return this.fileStats.origin || this.formContent.origin;
    },
    dateUploaded() {
      const date = this.fileStats.dateUploaded || this.formContent.dateUploaded;
      if (!date) return date;
      return new Date(date).toLocaleDateString();
    },
    dateModified() {
      const date = this.fileStats.dateModified || this.formContent.dateModified;
      if (!date) return date;
      return new Date(date).toLocaleDateString();
    },
    type() {
      return this.fileStats.type || this.formContent.type;
    },
    size() {
      return this.fileStats.size || this.formContent.size;
    },
    hasFiles() {
      return Object.keys(this.files).length > 0;
    },
  },
  watch: {
    value() {
      this.cancel();
    },
  },
  inject: ['trame'],
};
