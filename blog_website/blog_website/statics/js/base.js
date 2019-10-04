var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        cat_list: [],
        photo_categories: []

    },

    mounted() {

        this.get_cat();
        this.get_photo_categories();
    },
    methods: {

        get_cat() {
            var url = '/category/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.cat_list = response.data.cat_list;
                })
                .catch(error => {
                    console.log(error.response)
                })
        },

        get_photo_categories() {
            var url = '/photo/categories/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.photo_categories = response.data.photo_categories;
                })
                .catch(error => {
                    console.log(error.response)
                })
        },

    }
});