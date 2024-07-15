from deep_translator import GoogleTranslator
from sqlalchemy.orm import Session
from .models import TranslationTask


class Translation:
    def __init__(self, db: Session, args):
        self.__db = db
        self.__args = args

    def translate(self, task_id: str, text: str, languages: list):
        translated_arr = []
        for lang in languages:
            try:
                translated = GoogleTranslator(
                    source='auto', target=lang.strip()).translate(text.strip())
                translated_arr.append({lang: translated})
            except:
                translated_arr.append({lang: "Language is invalid."})
                print("Error in translation")

        return self.update_translation({"task_id": task_id, 'translation': translated_arr})

    def save_translation(self):
        task = TranslationTask(**self.__args)
        self.__db.add(task)
        self.__db.commit()
        self.__db.refresh(task)

        return task

    def update_translation(self, args):
        task = self.__db.query(TranslationTask).filter(
            TranslationTask.id == args.get('task_id', '')).first()
        task.translation = args.get('translation', [])
        task.status = 'completed'
        self.__db.commit()
        self.__db.refresh(task)

        return task

    def get_translation(self):
        task = self.__db.get(TranslationTask, self.__args.get('task_id', ''))
        if task is None:
            return None
        return task
