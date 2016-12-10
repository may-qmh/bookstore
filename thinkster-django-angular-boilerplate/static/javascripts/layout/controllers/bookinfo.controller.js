/**
* BookInfoController
* @namespace thinkster.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('thinkster.layout.controllers')
    .controller('BookInfoController', BookInfoController);

  BookInfoController.$inject = ['$scope', 'ShareVar'];

  /**
  * @namespace NavbarController
  */
  function BookInfoController($scope, ShareVar) {
    $scope.order = order;
    console.log("calling book info controller");

    function order(isbn10){
      console.log("function called");
      var n = document.getElementById("quantity").value;
      ShareVar.order_book(isbn10, n);
      console.log(n)

    }

  }
})();