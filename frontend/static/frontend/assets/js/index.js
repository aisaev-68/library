var mix = {
    methods: {
        getPopularBooks() {
            this.getData("/api/book/popular/")
              .then(data => {
                this.popularCards = data
              }).catch(() => {
                  this.popularCards = []
                  console.warn('Ошибка при получении списка популярных книг')
            })
        },
    },
    mounted() {
        this.getPopularBooks();
    },
    data() {
        return {
            popularCards: [],
        }
    }
}