var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {

        notice_list: [], // 公告数据,
        top_list: [],  // 点击排行
        recommend_list: [],  // 推荐
        article_count: '',
        pv: '',
        days: '',
        labels: [], // 标签

    },

    mounted() {
        this.get_notices();
        this.get_top();
        this.get_recommend();
        this.get_article_count();
        this.get_labels();


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
                    this.pv = response.data.pv;
                    this.days = response.data.days;
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