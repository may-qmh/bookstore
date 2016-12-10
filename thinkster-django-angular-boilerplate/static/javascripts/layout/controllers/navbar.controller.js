/**
* NavbarController
* @namespace thinkster.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('thinkster.layout.controllers')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['$scope', 'Authentication', 'ShareVar'];

  /**
  * @namespace NavbarController
  */
  function NavbarController($scope, Authentication, ShareVar) {
    var vm = this;

    vm.logout = logout;
    vm.search_books = search_books;
    vm.check_account = check_account;
    /**
    * @name logout
    * @desc Log the user out
    * @memberOf thinkster.layout.controllers.NavbarController
    */
    function logout() {
      Authentication.logout();
    }

    function search_books() {
      var author = vm.author;
      var publisher = vm.publisher;
      var title = vm.bk_title;
      var subject = vm.subject;
      console.log(ShareVar);
      ShareVar.search_books(vm.author,vm.publisher,vm.bk_title,vm.subject);
    }

    function check_account(username){
      console.log("checking account");
      Authentication.check_account(username);
    }
  }
})();