/**
* HomepageController
* @namespace thinkster.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('thinkster.layout.controllers')
    .controller('HomepageController', HomepageController);

  HomepageController.$inject = ['$scope', 'ShareVar'];

  /**
  * @namespace NavbarController
  */
  function HomepageController($scope, ShareVar) {
    $scope.select_book = select_book;


    function select_book(isbn10){
      
      ShareVar.get_book_info(isbn10);
      console.error(typeof isbn10)
    }

  }
})();