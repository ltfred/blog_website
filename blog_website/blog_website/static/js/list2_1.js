var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {

        top_list: [],  // 点击排行
        recommend_list: [],  // 推荐
        article_count: '',  // 文章统计
        cat_list: [],  // 分类
        labels: [], // 标签
    },

    mounted() {

        this.get_top();
        this.get_recommend();
        this.get_article_count();
        this.get_cat();
        this.get_labels();

    },
    methods: {

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

        get_labels() {
            var url = '/labels/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                    this.labels = response.data.labels;
                })
                .catch(error => {
                    console.log(error.response)
                })
        },

    }
});