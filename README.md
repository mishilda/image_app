# image_app

/create_new_experiment
создать конфигурацию тестирования
    dataset - варианты наборов картинок, пока не знаю, как их обозначать
    time_to_response - время на выбор ответа (в секундах)
    amount_of_pic - количество картинок из датасета, какое поведение при количестве большем, чем в датасете? выдавать все картинки или с повторами?
    config_name - имя конфигурации (необязательное поле), по умолчанию конфигурация сохраняется под автоматически генерируемым uuid
    конфигурация сохраняется в папку app/exp_config
/change_current_experiment
выбрать конфигурацию для проведения тестирования
создастся текстовый файл current, где хранится копия выбранной конфигурации

/new_quiz
начало нового тестирования

/start
при загрузке страницы производится выборка из датасета
перед нажатием start открыть нужные окна

/finish 
завершение тестирования и запись в файл
данные сессии (все ответы и данные о проходящем тестирование) очищаются


 