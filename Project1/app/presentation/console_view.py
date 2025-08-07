from .base import BaseView

class ConsoleView(BaseView):
    def show_help(self) -> str:
        help_text = """
Команди:
  add <ім'я> <номер телефону>     — додати контакт
  show all                        — показати всі контакти
  find <пошук>                    — знайти контакт
  exit                            — вихід
        """
        print(help_text)
        return help_text

    def show_contacts(self, contacts):
        if not contacts:
            result = "Контакти не знайдені."
        else:
            result = "\n".join([f"{c['name']}: {c['phone']}" for c in contacts])
        print(result)
        return result

    def show_message(self, message: str) -> str:
        print(message)
        return message
