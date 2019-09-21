var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {

        notice_list: [], // 公告数据,
        user_profile: '', // 用户数据
        top_list: [],  // 点击排行
        recommend_list: [],  // 推荐
        article_count: '',
        photo_categories: []

    },

    mounted() {
        this.get_notices();
        this.get_profile();
        this.get_top();
        this.get_recommend();
        this.get_article_count();
        this.get_photo_categories();


    },
    methods: {
        // 获取购物车数据
        get_notices() {
            var url = '/notices/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.notice_list = response.data.notice_list;

                })
                .catch(error => {
                    console.log(error.response);
                })
        },

        get_profile() {
            var url = '/profile/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.user_profile = response.data.profile;
                })
                .catch(error => {
                    console.log(error.response);
                })
        },

        get_top() {
            var url = '/top/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.top_list = response.data.top_list;
                })
                .catch(error => {
                    console.log(error.response)
                })
        },
        get_recommend() {
            var url = '/recommend/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.recommend_list = response.data.recommend_list;
                })
                .catch(error => {
                    console.log(error.response)
                })
        },

        get_article_count() {
            var url = '/article/count/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.article_count = response.data.article_count;
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