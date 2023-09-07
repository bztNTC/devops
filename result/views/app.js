var app = angular.module('taskApp', []);

app.controller('TaskController', function ($scope) {
  $scope.tasks = [];
  $scope.newTask = {};

  // Função para adicionar uma nova tarefa
  $scope.addTask = function () {
    if ($scope.newTask.title && $scope.newTask.description) {
      $scope.tasks.push({
        title: $scope.newTask.title,
        description: $scope.newTask.description,
        completed: false,
      });

      // Limpar os campos de entrada
      $scope.newTask = {};
    }
  };

  // Função para marcar uma tarefa como concluída
  $scope.completeTask = function (index) {
    $scope.tasks[index].completed = true;
  };

  // Função para remover tarefas concluídas
  $scope.removeCompletedTasks = function () {
    $scope.tasks = $scope.tasks.filter(function (task) {
      return !task.completed;
    });
  };
});
