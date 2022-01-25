export default {
  name: 'SearchItem',
  inject: ['get', 'properties', 'dirty'],
  computed: {
    description() {
      // FIXME Invalid if modified by server! dereference mtime
      return this.properties()['description'];
    },
    key() {
      // FIXME Invalid if modified by server! dereference mtime
      return this.properties()['key'];
    },
    value() {
      // FIXME Invalid if modified by server! dereference mtime
      return this.properties()['value'];
    },
  },
};
