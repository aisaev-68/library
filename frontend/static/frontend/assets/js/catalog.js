var mix = {
  methods: {
    setSort(id) {
      if (this.selectedSort?.id === id) {
        this.selectedSort.selected =
          this.selectedSort.selected === 'dec' ? 'inc' : 'dec';
      } else {
        if (this.selectedSort) {
          this.selectedSort = null;
        }
        this.selectedSort = this.sortRules.find((sort) => sort.id === id);
        this.selectedSort = {
          ...this.selectedSort,
          selected: 'dec',
        };
      }
      this.getBooks();
    },

    getBooks(page, filterSearch) {
          if (typeof page === 'undefined') {
            page = 1;
          }
      const PAGE_LIMIT = 6;
      const params = new URLSearchParams(window.location.search);

      params.set('page', page.toString());
      if (typeof filterSearch !== 'undefined') {
        params.set('filterSearch', filterSearch);
      }
      if (this.selectedSort) {
        params.set('sort', this.selectedSort.id);
        params.set('sortType', this.selectedSort.selected);
      }
      if (this.filter.name) {
        params.set('filter.name', this.filter.name);
      }
      if (this.filter.title) {
        params.set('filter.title', this.filter.title);
      }
      if (this.filter.genre) {
        params.set('filter.genre', this.filter.genre);
      }

      this.getData('/api/catalog/', {
        page,
        filterSearch: this.filterSearch ? this.filterSearch : null,
        genre: this.genre ? this.genre : null,
        sort: this.selectedSort ? this.selectedSort.id : null,
        sortType: this.selectedSort ? this.selectedSort.selected : null,
        filter: {
          name: this.filter.name ? this.filter.name : null,
          title: this.filter.title ? this.filter.title : null,
          genre: this.filter.genre ? this.filter.genre : null,
        },
        limit: PAGE_LIMIT,
      })
        .then((data) => {
          this.bookCards = data.items;
          this.currentPage = data.currentPage;
          this.lastPage = data.lastPage;
          this.resetFilters();
          const newURL = window.location.pathname + '?' + params.toString();

          window.history.replaceState(null, null, newURL);
        })
        .catch(() => {
          console.warn('Ошибка при получении книг');
        });
    },
    resetFilters() {
      this.filter = {
        name: '',
        title: '',
        genre: '',
      };
    },
  },
  mounted() {
    const urlParams = new URL(window.location.href).searchParams;
    this.filterSearch = urlParams.get('filterSearch');
    this.genre = urlParams.get('genre') ? Number(urlParams.get('genre')) : null;
    this.selectedSort = this.sortRules.find((sort) => sort.id === 'title');
    this.selectedSort.selected = 'inc';
    this.getBooks();
  },
  data() {
    return {
      pages: 1,
      filterSearch: '',
      genre: null,
      bookCards: [],
      currentPage: null,
      lastPage: 1,
      selectedSort: null,
      filter: {
        name: '',
        title: '',
        genre: '',
      },
      currentURL: window.location.href,
    };
  },
};


