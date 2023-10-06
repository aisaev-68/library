var mix = {
  methods: {
    getBook() {
      const bookId = location.pathname.startsWith('/book/') ?
        Number(location.pathname.replace('/book/', '').replace('/', '')) :
        null;
      this.getData(`/api/book/${bookId}/`)
        .then(data => {
          this.book = { ...this.book, ...data };
        })
        .catch(() => {
          this.book = {};
          console.warn('Ошибка при получении книг');
        });
    },
    submitReview() {
      const csrfToken = this.getCookie('csrftoken');
      this.postData(`/api/book/${this.book.id}/review/`, {
        text: this.review.text,
        rate: this.review.rate
      }, {
        headers: { 'X-CSRFToken': csrfToken }
      })
        .then(data => {
          this.book.reviews = data;
          this.review.text = '';
          this.review.rate = 5;
          this.getBook();
        })
        .catch(() => {
          console.warn('Ошибка при публикации отзыва');
        });
    },
  },
  mounted() {
    this.getBook();
  },
  data() {
    return {
      book: {},
      count: 1,
      review: {
        text: '',
        rate: 5
      }
    };
  }
};
