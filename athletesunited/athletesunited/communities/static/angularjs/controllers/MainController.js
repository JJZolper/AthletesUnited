
app.controller('MainController', ['$scope', 'CommunityPosts', function($scope, CommunityPosts) {
    $scope.communityposts = new CommunityPosts();
}]);




