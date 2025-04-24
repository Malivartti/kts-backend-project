-- Вставка темы
INSERT INTO theme (id, title) VALUES (1, 'География мира');

-- Вопрос 1
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (1, 1, 1, 'Какая страна является самой большой по площади?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (1, 'Китай', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (1, 'Соединенные Штаты Америки', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (1, 'Россия', true);

-- Вопрос 2
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (2, 1, 1, 'Какой океан самый большой?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (2, 'Атлантический', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (2, 'Тихий', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (2, 'Индийский', false);

-- Вопрос 3
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (3, 1, 1, 'Столица Франции - это:', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (3, 'Лондон', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (3, 'Париж', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (3, 'Берлин', false);

-- Вопрос 4
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (4, 1, 1, 'Какая река самая длинная в мире?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (4, 'Амазонка', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (4, 'Нил', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (4, 'Янцзы', false);

-- Вопрос 5
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (5, 1, 1, 'Какой континент самый холодный?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (5, 'Северная Америка', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (5, 'Арктика', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (5, 'Антарктида', true);

-- Вопрос 6
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (6, 1, 1, 'Столица Японии:', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (6, 'Сеул', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (6, 'Пекин', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (6, 'Токио', true);

-- Вопрос 7
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (7, 1, 1, 'В какой стране находится Эйфелева башня?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (7, 'Италия', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (7, 'Франция', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (7, 'Испания', false);

-- Вопрос 8
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (8, 1, 1, 'Какая гора самая высокая в мире?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (8, 'Монблан', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (8, 'Эльбрус', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (8, 'Эверест', true);

-- Вопрос 9
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (9, 1, 1, 'Какой материк самый маленький?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (9, 'Австралия', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (9, 'Антарктида', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (9, 'Европа', false);

-- Вопрос 10
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (10, 1, 1, 'Через какую страну проходит экватор?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (10, 'Россия', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (10, 'Бразилия', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (10, 'Канада', false);

-- Вопрос 11
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (11, 1, 1, 'Самое большое озеро в мире по площади:', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (11, 'Байкал', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (11, 'Каспийское море', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (11, 'Виктория', false);

-- Вопрос 12
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (12, 1, 1, 'Столица Италии:', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (12, 'Милан', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (12, 'Рим', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (12, 'Венеция', false);

-- Вопрос 13
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (13, 1, 1, 'Какой из этих городов является столицей Австралии?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (13, 'Сидней', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (13, 'Мельбурн', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (13, 'Канберра', true);

-- Вопрос 14
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (14, 1, 1, 'Великая Китайская стена находится в:', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (14, 'Японии', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (14, 'Китае', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (14, 'Монголии', false);

-- Вопрос 15
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (15, 1, 1, 'Какое море является самым солёным?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (15, 'Черное море', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (15, 'Красное море', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (15, 'Мертвое море', true);

-- Вопрос 16
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (16, 1, 1, 'Назовите столицу Великобритании.', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (16, 'Лондон', true);

-- Вопрос 17
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (17, 1, 1, 'Какая река протекает через Москву?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (17, 'Москва-река', true);

-- Вопрос 18
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (18, 1, 1, 'На каком континенте находится Египет?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (18, 'Африка', true);

-- Вопрос 19
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (19, 1, 1, 'Назовите самый большой остров в мире.', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (19, 'Гренландия', true);

-- Вопрос 20
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (20, 1, 1, 'Какая страна имеет форму сапога?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (20, 'Италия', true);

-- Вопрос 21
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (21, 1, 1, 'Какое озеро является самым глубоким в мире?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (21, 'Байкал', true);

-- Вопрос 22
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (22, 1, 1, 'Назовите столицу Германии.', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (22, 'Берлин', true);

-- Вопрос 23
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (23, 1, 1, 'В какой стране находится Великая пирамида Гизы?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (23, 'Египет', true);

-- Вопрос 24
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (24, 1, 1, 'Какой город является столицей Нидерландов?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (24, 'Амстердам', true);

-- Вопрос 25
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (25, 1, 1, 'Какая пустыня является самой большой в мире?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (25, 'Сахара', true);

-- Вопрос 26
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (26, 1, 1, 'В какой стране находится Тадж-Махал?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (26, 'Индия', true);

-- Вопрос 27
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (27, 1, 1, 'Назовите самый маленький континент.', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (27, 'Австралия', true);

-- Вопрос 28
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (28, 1, 1, 'Сколько океанов существует на Земле?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (28, '5', true);

-- Вопрос 29
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (29, 1, 1, 'Назовите самую длинную реку в Европе.', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (29, 'Волга', true);

-- Вопрос 30
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (30, 1, 1, 'В какой стране находится город Рио-де-Жанейро?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (30, 'Бразилия', true);

-- Вставка темы
INSERT INTO theme (id, title) VALUES (2, 'История России');

-- Вопрос 1
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (31, 1, 2, 'Кто был первым русским царем?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (31, 'Петр I', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (31, 'Иван Грозный', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (31, 'Александр I', false);

-- Вопрос 2
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (32, 1, 2, 'В каком городе была столица Древней Руси?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (32, 'Москва', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (32, 'Киев', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (32, 'Новгород', false);

-- Вопрос 3
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (33, 1, 2, 'Какой русский император основал Санкт-Петербург?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (33, 'Николай II', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (33, 'Александр II', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (33, 'Пётр I', true);

-- Вопрос 4
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (34, 1, 2, 'В каком году началась Великая Отечественная война?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (34, '1939', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (34, '1941', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (34, '1945', false);

-- Вопрос 5
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (35, 1, 2, 'Кто был первым человеком в космосе?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (35, 'Нил Армстронг', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (35, 'Алексей Леонов', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (35, 'Юрий Гагарин', true);

-- Вопрос 6
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (36, 1, 2, 'В каком веке произошло Крещение Руси?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (36, 'X век', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (36, 'IX век', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (36, 'XI век', false);

-- Вопрос 7
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (37, 1, 2, 'Кто руководил СССР во время Великой Отечественной войны?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (37, 'Ленин', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (37, 'Сталин', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (37, 'Хрущев', false);

-- Вопрос 8
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (38, 1, 2, 'В каком году распался СССР?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (38, '1985', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (38, '1991', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (38, '1993', false);

-- Вопрос 9
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (39, 1, 2, 'Какое прозвище было у князя Александра?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (39, 'Мудрый', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (39, 'Великий', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (39, 'Невский', true);

-- Вопрос 10
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (40, 1, 2, 'Кто был последним российским императором?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (40, 'Александр III', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (40, 'Павел I', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (40, 'Николай II', true);

-- Вопрос 11
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (41, 1, 2, 'В каком году отменили крепостное право в России?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (41, '1861', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (41, '1812', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (41, '1905', false);

-- Вопрос 12
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (42, 1, 2, 'Кто из русских ученых создал таблицу химических элементов?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (42, 'Павлов', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (42, 'Менделеев', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (42, 'Ломоносов', false);

-- Вопрос 13
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (43, 1, 2, 'В каком году была основана Москва (согласно летописи)?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (43, '1147', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (43, '1237', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (43, '988', false);

-- Вопрос 14
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (44, 1, 2, 'Кто командовал русскими войсками во время Отечественной войны 1812 года?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (44, 'Суворов', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (44, 'Кутузов', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (44, 'Жуков', false);

-- Вопрос 15
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (45, 1, 2, 'В каком веке правил Петр I?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (45, 'XVII-XVIII вв.', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (45, 'XVI-XVII вв.', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (45, 'XVIII-XIX вв.', false);

-- Вопрос 16
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (46, 1, 2, 'Назовите имя первого президента России (Имя Фамилия).', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (46, 'Борис Ельцин', true);

-- Вопрос 17
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (47, 1, 2, 'В каком году произошла Октябрьская революция?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (47, '1917', true);

-- Вопрос 18
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (48, 1, 2, 'Кто написал произведение "Война и мир" (Имя Фамилия)?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (48, 'Лев Толстой', true);

-- Вопрос 19
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (49, 1, 2, 'Как звали князя, который правил во время Крещения Руси (Имя)?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (49, 'Владимир', true);

-- Вопрос 20
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (50, 1, 2, 'Какое событие произошло в 1812 году?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (50, 'Отечественная война', true);

-- Вопрос 21
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (51, 1, 2, 'Кто был главным конструктором первого спутника Земли (Имя Фамилия)?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (51, 'Сергей Королев', true);

-- Вопрос 22
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (52, 1, 2, 'В каком году была Куликовская битва?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (52, '1380', true);

-- Вопрос 23
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (53, 1, 2, 'Кто основал город Москву в 1147 году (Имя Фамилия)?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (53, 'Долгорукий', true);

-- Вопрос 24
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (54, 1, 2, 'В каком году произошла Великая Октябрьская социалистическая революция?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (54, '1917', true);

-- Вопрос 25
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (55, 1, 2, 'Кто был создателем первой в России государственной публичной библиотеки?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (55, 'Екатерина II', true);

-- Вопрос 26
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (56, 1, 2, 'Какой династии начал править в России с 1613 года?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (56, 'Романовы', true);

-- Вопрос 27
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (57, 1, 2, 'Кто был супругом Екатерины II?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (57, 'Петр III', true);

-- Вопрос 28
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (58, 1, 2, 'Кто победил в Северной войне?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (58, 'Россия', true);

-- Вопрос 29
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (59, 1, 2, 'В каком году Россия приняла участие в Первой мировой войне?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (59, '1914', true);

-- Вопрос 30
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (60, 1, 2, 'Как назывался первый русский университет?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (60, 'Московский', true);

-- Вставка темы
INSERT INTO theme (id, title) VALUES (3, 'Кино и мультфильмы');

-- Вопрос 1
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (61, 1, 3, 'Кто режиссер фильма "Титаник"?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (61, 'Стивен Спилберг', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (61, 'Джеймс Кэмерон', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (61, 'Кристофер Нолан', false);

-- Вопрос 2
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (62, 1, 3, 'Какой мультфильм рассказывает о львенке по имени Симба?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (62, 'Мадагаскар', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (62, 'Король Лев', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (62, 'Шрек', false);

-- Вопрос 3
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (63, 1, 3, 'Кто сыграл Гарри Поттера в одноименной серии фильмов?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (63, 'Руперт Гринт', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (63, 'Дэниел Рэдклифф', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (63, 'Том Фелтон', false);

-- Вопрос 4
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (64, 1, 3, 'Какой фильм получил Оскар за лучший фильм в 2020 году?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (64, '1917', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (64, 'Джокер', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (64, 'Паразиты', true);

-- Вопрос 5
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (65, 1, 3, 'Как зовут главного героя в мультфильме "Шрек"?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (65, 'Осел', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (65, 'Шрек', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (65, 'Фиона', false);

-- Вопрос 6
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (66, 1, 3, 'Кто озвучивал Джинна в оригинальном мультфильме "Аладдин"?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (66, 'Джим Керри', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (66, 'Робин Уильямс', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (66, 'Эдди Мерфи', false);

-- Вопрос 7
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (67, 1, 3, 'Кто режиссер фильма "Аватар"?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (67, 'Питер Джексон', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (67, 'Джеймс Кэмерон', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (67, 'Джордж Лукас', false);

-- Вопрос 8
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (68, 1, 3, 'В каком фильме звучит фраза "Я вернусь"?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (68, 'Рэмбо', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (68, 'Терминатор', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (68, 'Крепкий орешек', false);

-- Вопрос 9
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (69, 1, 3, 'Какая студия создала мультфильмы "Холодное сердце" и "Рапунцель"?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (69, 'DreamWorks', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (69, 'Pixar', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (69, 'Disney', true);

-- Вопрос 10
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (70, 1, 3, 'Кто режиссер фильма "Властелин колец"?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (70, 'Кристофер Нолан', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (70, 'Питер Джексон', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (70, 'Джеймс Кэмерон', false);

-- Вопрос 11
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (71, 1, 3, 'Какой российский мультфильм рассказывает о приключениях Чебурашки?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (71, 'Простоквашино', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (71, 'Крокодил Гена и Чебурашка', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (71, 'Винни Пух', false);

-- Вопрос 12
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (72, 1, 3, 'Как называется космический корабль в "Звездных войнах" Хана Соло?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (72, 'Энтерпрайз', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (72, 'Сокол Тысячелетия', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (72, 'Звезда Смерти', false);

-- Вопрос 13
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (73, 1, 3, 'Какой актер играл Тони Старка в фильмах Marvel?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (73, 'Крис Эванс', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (73, 'Роберт Дауни-младший', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (73, 'Крис Хемсворт', false);

-- Вопрос 14
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (74, 1, 3, 'Кто из этих персонажей является злодеем в "Короле Льве"?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (74, 'Муфаса', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (74, 'Шрам', true);
INSERT INTO answer (question_id, title, is_correct) VALUES (74, 'Рафики', false);

-- Вопрос 15
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (75, 1, 3, 'Какой фильм начинается с сцены в Новой Зеландии и заканчивается в Нью-Йорке?', 'MULTI');
INSERT INTO answer (question_id, title, is_correct) VALUES (75, 'Интерстеллар', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (75, 'Властелин колец', false);
INSERT INTO answer (question_id, title, is_correct) VALUES (75, 'Кинг-Конг', true);

-- Вопрос 16
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (76, 1, 3, 'Назовите один из самых известных фильмов Стивена Спилберга про динозавров.', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (76, 'Парк юрского периода ', true);

-- Вопрос 17
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (77, 1, 3, 'Кто сыграл главную роль в фильме "Матрица" (Имя Фамилия)?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (77, 'Киану Ривз', true);

-- Вопрос 18
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (78, 1, 3, 'Назовите самый кассовый фильм всех времен.', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (78, 'Аватар', true);

-- Вопрос 19
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (79, 1, 3, 'Какая компания создала мультфильм "История игрушек"?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (79, 'Pixar', true);

-- Вопрос 20
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (80, 1, 3, 'Как зовут отца Симбы в мультфильме «Король Лев»?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (80, 'Муфаса', true);

-- Вопрос 21
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (81, 1, 3, 'В каком подводном городе живёт главный герой мультсериала «Губка Боб Квадратные Штаны»?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (81, 'Бикини Боттом', true);

-- Вопрос 22
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (82, 1, 3, 'В какой стране родился персонаж Джеймс Бонд по сюжету фильмов??', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (82, 'Англия', true);

-- Вопрос 23
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (83, 1, 3, 'В какой стране был создан мультфильм «Ну, погоди!»?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (83, 'СССР', true);

-- Вопрос 24
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (84, 1, 3, 'Как зовут главного героя мультфильма "Пиноккио" студии Disney?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (84, 'Пиноккио', true);

-- Вопрос 25
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (85, 1, 3, 'Кто является создателем киновселенной Marvel? (Имя Фамилия)', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (85, 'Стэн Ли', true);

-- Вопрос 26
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (86, 1, 3, 'Назовите имя героя, которого играет Леонардо Ди Каприо в фильме "Титаник" (Имя Фамилия).', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (86, 'Джек Доусон', true);

-- Вопрос 27
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (87, 1, 3, 'Кто озвучивал Машу в мультфильме "Маша и Медведь" (Имя Фамилия)?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (87, 'Алина Кукушкина', true);

-- Вопрос 28
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (88, 1, 3, 'В каком году вышел первый фильм о Гарри Поттере?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (88, '2001', true);

-- Вопрос 29
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (89, 1, 3, 'Как зовут главного персонажа мультфильма "Шрек"?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (89, 'Шрек', true);

-- Вопрос 30
INSERT INTO question (id, user_id, theme_id, title, type) VALUES (90, 1, 3, 'Кто режиссер фильма "Броненосец Потемкин (Имя Фамилия)"?', 'SINGLE');
INSERT INTO answer (question_id, title, is_correct) VALUES (90, 'Сергей Эйзенштейн', true);
