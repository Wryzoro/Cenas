from task import Task, TaskManager

def display_menu():
    print("To-do List:")
    print("==============")
    print("1. Adicionar tarefa")
    print("2. Remover tarefa")
    print("3. Completar tarefa")
    print("4. Mostrar todas as tarefas")
    print("5. Mostrar tarefas pendentes")
    print("6. Mostrar tarefas concluídas")
    print("7. Sair")
    print("==============")

def display_tasks(tasks, title):
    print(f"\n{title}")
    for i, task in enumerate(tasks):
        status = "v (Concluida)" if task.completed else "x (Não Concluida)"
        print(f"{i + 1}. {task.title} - {task.description} [{status}]")
    input("\nPressione Enter para voltar ao menu principal...")

def main():
    task_manager = TaskManager()
    while True:
        display_menu()
        choice = input("Escolha uma opção: ")
        if choice == '1':
            title = input("Título da tarefa: ")
            description = input("Descrição da tarefa : ")
            task = Task(title, description)
            task_manager.add_task(task)
        elif choice == '2':
            index = int(input("Índice da tarefa a ser removida: ")) - 1
            task_manager.remove_task(index)
        elif choice == '3':
            index = int(input("Índice da tarefa a ser completada: ")) - 1
            task_manager.complete_task(index)
        elif choice == '4':
            display_tasks(task_manager.tasks, "Todas as Tarefas:")
        elif choice == '5':
            pending_tasks = [task for task in task_manager.tasks if not task.completed]
            display_tasks(pending_tasks, "Tarefas Pendentes:")
        elif choice == '6':
            completed_tasks = [task for task in task_manager.tasks if task.completed]
            display_tasks(completed_tasks, "Tarefas Concluídas:")
        elif choice == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida, por favor escolha novamente.")

if __name__ == "__main__":
    main()