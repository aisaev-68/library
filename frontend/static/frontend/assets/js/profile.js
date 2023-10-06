var mix = {
  methods: {
    getProfile() {
      // Получение профиля
      const csrfToken = this.getCookie('csrftoken');
      this.getData('/api/profile/', {
        headers: { 'X-CSRFToken': csrfToken }
      })
        .then(data => {
          this.fullName = data.fullName;
          this.avatar = data.avatar;
          this.phone = data.phone;
          this.email = data.email;

        })
        .catch(() => {
          console.warn('Ошибка при получении профиля');
        });
    },

    changeProfile() {
      // Очистка предыдущих ошибок
      this.clearErrors();

      // Обновление профиля
      if (!this.fullName.trim().length) {
        const fullNameInput = document.querySelector('#name');
        fullNameInput.classList.add('error');
        fullNameInput.insertAdjacentHTML('afterend', `<span class="error-text">Поле ФИО должно быть заполнено</span>`);
      }

      const emailInput = document.querySelector('#email');
      if (!this.email.trim().length) {
        emailInput.classList.add('error');
        emailInput.insertAdjacentHTML('afterend', `<span class="error-text">Поле E-mail должно быть заполнено</span>`);
      } else if (!this.isEmailValid(this.email)) {
        emailInput.classList.add('error');
        emailInput.insertAdjacentHTML('afterend', `<span class="error-text">Некорректный адрес электронной почты</span>`);
      }

      const errorFields = document.querySelectorAll('.error');
      if (errorFields.length > 0) {
        return;
      }

      const csrfToken = this.getCookie('csrftoken');
      this.postData(
        '/api/profile/',
        {
          fullName: this.fullName,
          phone: this.phone,
          email: this.email,

        },
        { headers: { 'X-CSRFToken': csrfToken } }
      )
        .then(({ data }) => {
          // Если нет ошибок, выполняем необходимые действия

          this.fullName = data.fullName;
          this.phone = data.phone;
          this.email = data.email;
          //alert('Успешно сохранено');

          // Очищаем поля от ошибок
          this.clearErrors();

        })
        .catch(() => {
          console.warn('Ошибка при обновлении профиля');
        });
        this.profileUpdated = true;
    },

    changePassword() {
      // Очистка предыдущих ошибок
      this.clearErrors();

      // Изменение пароля
      if (
        !this.passwordCurrent.trim().length ||
        !this.password.trim().length ||
        !this.passwordReply.trim().length ||
        this.password !== this.passwordReply
      ) {
        alert('В форме присутствуют незаполненные поля или пароли не совпадают');
        return;
      }

      const csrfToken = this.getCookie('csrftoken');
      this.postData(
        '/api/profile/password/',
        {
          passwordCurrent: this.passwordCurrent,
          password: this.password,
          passwordReply: this.passwordReply
        },
        { headers: { 'X-CSRFToken': csrfToken } }
      )
        .then(data => {
          // Если нет ошибок, выполняем необходимые действия
          alert('Успешно сохранено');
          this.passwordCurrent = '';
          this.password = '';
          this.passwordReply = '';
          this.passwordUpdated = true;
        })
        .catch(error => {
          this.passwordError = true;
          this.passwordCurrent = '';
          this.password = '';
          this.passwordReply = '';
          console.warn('Ошибка при сохранении пароля');
        });

    },

    setAvatar(event) {
      // Загрузка изображения
      const target = event.target;
      const file = target.files && target.files[0] ? target.files[0] : null;
      if (!file) return;

      const formData = new FormData();
      formData.append('avatar', file);

      const csrfToken = this.getCookie('csrftoken');
      this.postData('/api/profile/avatar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': csrfToken
        }
      })
        .then(data => {
          this.avatar = data.url;
        })
        .catch(() => {
          console.warn('Ошибка при обновлении изображения');
        });
        this.avatarUpdated = true;
    },

    getCookie(name) {
      // Получение значения куки по имени
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    clearAvatar() {
      this.avatar = null;
    },

    clearErrors() {
      // Очистка ошибок
      const errorFields = document.querySelectorAll('.error');
      errorFields.forEach(field => {
        field.classList.remove('error');
      });

      const errorTextElements = document.querySelectorAll('.error-text');
      errorTextElements.forEach(element => {
        element.remove();
      });
    },

    isEmailValid(email) {
      // Проверка корректности email-адреса
      // В данном примере, проверяем простейший шаблон адреса
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailPattern.test(email);
    }
  },

  created() {
    this.getProfile();
  },

  data() {
    return {
      fullName: '',
      phone: '',
      email: '',
      avatar: '',
      password: '',
      passwordCurrent: '',
      passwordReply: '',
      profileUpdated: false,
      avatarUpdated: false,
      passwordUpdated: false,
      passwordError: false
    };
  }
};

