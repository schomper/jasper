var portalApp = angular.module('portalApp',
                              ['ngRoute',
                               'ui.bootstrap']);

portalApp.config(function($routeProvider){
    $routeProvider.
        when('/', {
            templateUrl: 'templates/article-list.html',
            controller: 'ArticleListCtrl'
        }).
        when('/topics', {
            templateUrl: 'templates/topic-info.html',
            controller: 'TopicInfoCtrl'
        }).
        otherwise({
            redirectTo: '/'
        });
});
