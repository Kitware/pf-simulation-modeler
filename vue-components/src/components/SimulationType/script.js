export default {
  name: 'SimulationType',
  props: ['value'],
  data() {
    return {
      formContent: { ...(this.value || {}) },
    };
  },
  methods: {
    updateFormContent() {
      this.$emit('input', { ...this.formContent });
    },
  },
};
