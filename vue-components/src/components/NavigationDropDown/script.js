export default {
  name: 'NavigationDropDown',
  props: ['value', 'views'],
  data: () => ({}),
  computed: {
    canMoveForward() {
      const i = this.views.indexOf(this.value);
      return i !== -1 && i < this.views.length - 1;
    },
    canMoveBackward() {
      const i = this.views.indexOf(this.value);
      return i !== -1 && i > 0;
    },
  },
  methods: {
    moveBackward() {
      const i = this.views.indexOf(this.value);
      this.$emit('input', this.views[i - 1]);
    },
    moveForward() {
      const i = this.views.indexOf(this.value);
      this.$emit('input', this.views[i + 1]);
    },
  },
};
