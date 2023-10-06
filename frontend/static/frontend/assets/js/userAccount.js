var mix = {
  methods: {
    getUserAccount() {
      const csrfToken = this.getCookie('csrftoken');
      this.getData("/api/account/", {
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
        .then(data => {
          this.firstname = data.first_name;
          this.lastname = data.last_name;
          this.surname = data.surname;
          this.avatar = data.avatar;
        });
    },
  },

  mounted() {
    this.getUserAccount();
  },
  data() {
    return {
      lastname: "",
      firstname: "",
      surname: "",
      avatar: "",
    };
  },
  computed: {
    fullName() {
      return [this.lastname, this.firstname, this.surname].join(" ");
    },
    displayContent() {
      return this.avatar ? this.avatar : this.fullName;
    },
  },
};
