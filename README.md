# F2 Выпускной проект 
Веб-сайт Система проведения опросов.

В проекте изпользуются: фреймворк Django, Bootstrap, база данных PostgreSQL и NGINX для публикации.
Проект развёрнут на виртуальном сервере на хостинге и доступен по адресу: http://f2.us.to

В проекте доступно три типа пользователей:
1. Обычные пользователи - сами регистрируются на сайте, проходят опросы и могут смотреть только свою статистику.
2. Составители опросов(HR) - права пользователя устанавливает superuser или другой HR, эти пользователи так же могут проходить опросы, могут создавать вопросы и опросы, а так же просмтаривать статистику по любому пользователю.
3. Superuser - пользователь, который имеет максимальные полномочия в системе опросов и доступ в админку django. 

Для проверки проекта созданы следующие пользователи:
- superuser с паролем skillfactory_f2
- user с паролем P@ssw0rd1 (имеет полномочия HR)
- user1 с паролем P@ssw0rd1 (обычный пользователь без полномочий)

Сайт имеет изменяемое наполнение в зависимости от полномочий пользователя:
1. Обычные пользователи имеют доступ к следующим страницам:
    - http://f2.us.to/ - главная страница с кратким описанием сайта
    - http://f2.us.to/user_create/ - страница регистрации нового пользователя
    - http://f2.us.to/login/ - страница для входа пользователя
    - http://f2.us.to/logout/ - ссылка для выхода пользователя
    - http://f2.us.to/user_poll_choice/ - страница со всеми доступными опросами и выбором опроса для прохождения
    - http://f2.us.to/user_statistics/ - страница со статистикой и списком опросов, вопросов и ответов пройденных пользователем

2. Персоналу HR доступен функционал:
    - http://http://f2.us.to/users_management/ - страница управления пользователями, доступна функция выбора персонал HR, создания, удаления, изменения пользователя
    - http://f2.us.to/hr_statistic/user_id/ - страница со статистикой пользователя для персонала HR
    - http://f2.us.to/user_update/user_id/ - страница, на которой можно изменить имя, фамилию и логин любого пользователя
    - http://f2.us.to/user_delete/user_id/ - страница удаления пользователя
    - http://f2.us.to/poll_list/ - перечень всех созданных опросов
    - http://f2.us.to/question_list/ - перечень всех созданных вопросов
    - http://f2.us.to/poll_create/ - страница создания нового опроса
    - http://f2.us.to/question_create/ - страница создания нового вопроса
    - http://f2.us.to/question_choice_list/poll_id/question_in_poll_id/ - интерфейс управления опросами, добавить, удалить, назначить баллы и т.д.

Работа с сайтом.
1. Личный кабинет составителя опросов реализован в web-интерфейсе сайта. Можно сразу создавать опрос, а затем выбирать вопросы или создавать новые.
2. Вопросы могут быть двух вариантов: выбор одного ответа из четырёх вариантов и выбор нескольких ответов из четырёх вариантов. 
3. Можно добавлять картинку к вопросу.
4. Вопросы можно объединять в разные опросы. Один и тот же вопрос может быть добавлен в несколько опросов.
5. Для каждого вопроса внутри опроса можно задавать баллы, таким образом ответы на один и тот же вопрос в разных опросах могут давать разное количество баллов.
6. У каждого опроса есть дата публикации, до наступления которой он является недоступным для пользователя. 
7. В интерфейсе управлнеия опросами для HR возможно фильтровать вопросы по типам - много ответов или один ответ.
8. У каждого пользователя на странице с опросами отображается информация о прохождении опросов и в персональной статистике о набранных баллах и ответах на пройденные вопросы.
9. На странице статистики пользователь может посмотреть сколько опросов пройдено, сколько еще доступно; сколько баллов он набрал; минимальный и максимальный балл за ответ на вопрос; общий рейтинг прохождения опросов в сравнении с другими пользователями; а так же подробная информация о том, какие ответы были даны на вопросы во всех пройденных опросах. Пользователи с привилегией HR и superuser помимо просмотра своих данных имеют возможность просмотреть статистику по любому пользователю.
10. На странице управления пользователями, специалист HR может видеть общую статистику прохождения опросов, управлять учетными записями и просматривать статистику по каждому пользователю.

Система опросов реализована в виде мультисервисной архитектуры на основе контейнеров Docker и для запуска на локальном компьютере или сервере должен поддерживаться этот функционал.

Для запуска контейнеров:
- скопировать проект с Github
- перейти в папку с проектом и выполнить команду docker-compose build 
- после успешной сборки контейнеров запустить их командой docker-compose up
- сервер будет доступен по HTTP порт-80. 

Для разработки, имеется возможность локального запуска django проекта, для этого нужно выполнить шаги:
- скачать проект с GitHub
- перейти в папку с проектом
- создать виртуальное окружение: $ python -m venv venv
- применить виртуальное окружение: source venv/bin/activate
- перейти в папку poll_system и установить зависимости: pip install -r requirements.txt 
- внести изменения в файл настроек проекта settings.py - настроить раздел DATABASES
- выполнить миграции:
    - python manage.py makemigrations
    - python manage.py migrate
- создать суперпользователя: python manage.py createsuperuser
- запустить сервер: python manage.py runserver