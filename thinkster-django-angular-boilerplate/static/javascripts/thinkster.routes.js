(function () {
  'use strict';

  angular
    .module('thinkster.routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
    $routeProvider
    .when('/register', {
      controller: 'RegisterController', 
      controllerAs: 'vm',
      templateUrl: 'static/templates/authentication/register.html'
    })
    .when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: 'static/templates/authentication/login.html'
    })
    .when('/search', {
      controller: 'NavbarController',
      controllerAs: 'vm',
      templateUrl: 'static/templates/books/search.html'
    })
    .when('/',{
      controller: 'HomepageController',
      controllerAs: 'vm',
      templateUrl: 'templates/homepage.html'      
    })
    .when('/book/',{
      controller: 'BookInfoController',
      controllerAs: 'vm',
      templateUrl: 'templates/book_info.html'
    })
    .when('/account/',{
      controller: 'UserInfoController',
      controllerAs: 'vm',
      templateUrl: 'templates/user_info.html'
    })
    .otherwise('/');

    
  }
})();

