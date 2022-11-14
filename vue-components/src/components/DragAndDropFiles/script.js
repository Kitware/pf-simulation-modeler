export default {
  name: 'DragNDropFiles',
  props: ['file', 'disabled'],
  data: () => ({
    dragging: false,
  }),
  methods: {
    onChange(e) {
      var files = e.target.files || e.dataTransfer.files;

      this.dragging = false;

      if (this.disabled) {
        return;
      }

      if (!files.length) {
        return;
      }

      this.createFile(files[0]);
    },
    createFile(file) {
      this.$emit('uploaded', file);
    },
    removeFile() {
      this.createFile(undefined);
    },
  },
  computed: {
    extension() {
      return this.file ? this.file.name.split('.').pop() : '';
    },
  },
};
