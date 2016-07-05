
app.factory('CommunityPosts', ['$http', function($http) {
                               
    var _page = 0;
                               
    console.log("lol");
                               
    var CommunityPosts = function() {
        this.items;
        this.busy = false;
    };
                               
    console.log("lol2");
                               
    CommunityPosts.prototype.loadmore = function() {
        if (this.busy) return;
        this.busy = true;
                               
        _page++;

        var url = "http://127.0.0.1:8000/api/communityposts/?format=json&page=" + _page + "&jsonp=JSON_CALLBACK";
        $http.jsonp(url).success(function(data) {
            console.log(data);
            var items = data;
            for (var i = 0; i < items.length; i++) {
                this.items.push(items[i].data);
            }
            this.busy = false;
        }.bind(this));
    };
                               
    return CommunityPosts;
}]);


// app.factory('CommunityPosts', ['$http', function($http) {
//    return $http.get('http://127.0.0.1:8000/api/communityposts/?format=json')
//        .success(function(data) {
//            return data;
//        })
//        .error(function(err) {
//            return err;
//        });




















// Reddit constructor function to encapsulate HTTP and pagination logic
//myApp.factory('Reddit', function($http) {
//    var Reddit = function() {
//        this.items = [];
//        this.busy = false;
//        this.after = '';
//    };
//
//    Reddit.prototype.loadmore = function() {
//        if (this.busy) return;
//        this.busy = true;
//
//        var url = "http://api.reddit.com/hot?after=" + this.after + "&jsonp=JSON_CALLBACK";
//        $http.jsonp(url).success(function(data) {
//            var items = data.data.children;
//            for (var i = 0; i < items.length; i++) {
//                this.items.push(items[i].data);
//            }
//            this.after = "t3_" + this.items[this.items.length - 1].id;
//            this.busy = false;
//        }.bind(this));
//    };
//
//    return Reddit;
//});




