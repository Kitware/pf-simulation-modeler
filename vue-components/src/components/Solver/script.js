import SearchItem from '../SearchItem';

export default {
  name: 'Solver',
  data: () => ({ searchQuery: '' }),
  components: {
    SearchItem,
  },
  props: ['search', 'ids'],
  inject: ['get'],
  computed: {
    simputIds() {
      return this.get(this.ids);
    },
  },
  methods: {
    searchMatch(id) {
      return this.get(this.search)[id].search(this.searchQuery) > -1;
    },
  },
};
