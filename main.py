
import os
import json
from classify import QuestionPaser

codes = {'10000000000000011010000100000000000010000000000000000', '10000000000000011110000100000000000110000000000000100', '00000000000000000010000000000000000000000000000000000', '11100001011000001110000000000000000110000000000000100', '10000000000000000010000100000000000110000000000000000', '10000000000000000010000000000100000010000000000000000', '00010000000000000000000000010000000001000000000000000', '01100010000000011010000100000000000100000000000000000', '00000000000000000010000000000000000001000000000000000', '10000000000000011010000000000000000010000000000000000', '10000000001000000011000000000100000010000000000000000', '01100010000000011000000000000000000101000001100000000', '01100010000000011010000100000000000100100000000000000', '10000000000000011110000101010000000110000000000000100', '01110000000001011100000000000000000001000001000000000', '01110000000000011110000100000000000000000000000000000', '00000000001000000010100000000000000000000000000000001', '00000001011000011110000000000000000001000000000000000', '00000000000000001110000000010000000000000000000000000', '00010000011000000010000000000000000000000000000001000', '00000001001000000010000000010000000001000001000000000', '00000000000000000000000000000000000001000001000100000', '10000000000000000010000000000000000010001000000000000', '00000001000000000010000100000000010100000000000000000', '10010001001000000010000000000100100010000000000000000', '00010011011010011110000000000000000000000000000000000', '00010000000000000000001000000000000001000001000000000', '10000000000000011110000000000000000111000001000000100', '00000011011000011110010100000000000000000000000000000', '00000000000000001100000000000000000001000001000000000', '00000000000000011110000100010000000000000000000000000', '00000000000000011110000100000000000000000000000000000', '00000000000000011110000100000000000000000000000000010', '00000001001000000000000000000000000001000001000000000', '00000000001100000000000000000000000000000000000000000', '00000000001100000010000000000000000000000000000000000', '01100010000000011110000100000000000100100000000000000', '00000000000000000000000000010000000001000001000000000', '00000010000000011010000100000000000100000000000000000', '10000000000000001010000000000000000010000000000000000', '10000000000000000000000000000100000010000000000000000', '00010000000000000010000010000000001100000000000000000', '10000000000000000000000000000000000111000001000000000', '00000001001000000000000000010001000001000001000000000', '00010001001000000000000000000001100001000001000000000', '00010000000000001110000000000000000000000100000000000', '00000000000000000010000000000000000001000001000000000', '00010001001000000000000000000000000000000000000000000', '00000001011000011100000000000000000001000001000000000', '10000000100000000000000000000100000010000000000000000', '00000000000000001110000000000000000000000000000000000', '10000000000000000000000000000000000000000000000100000', '00000000000000000000000000000000000001000001000000000', '00000000000000000000000000000000000101000001000000000', '00010000000000001110000000000000000100000000000010000', '00000000000000000000000000000000000001000001010000000', '00010000000000011010000010000000001100000000000000000', '10000000000001001110000000000000000110000000000000100', '00010011011010011110000000000000001000000000000000000', '00000000000000001100000000000000000000000000000000000', '00000001001000000010000000000000000001000000000000000', '01100000000000011000000000000000000100100000000000000', '00000000000000000000000000000000000001000000000000000', '01110010000000011000000010000000000101010001000000000', '00000000000000000010000000000000000001010001000000000', '01100000000000011000000000000000000001000001100000000', '00000000000000000000000000010000000000000000000000000', '00000000001000000000000000000000000001000000000000000', '00000000000000011110000000000000000001000001000000000', '01110000000000011110000010000000001100000000000000000', '00010001001000000010000010000001100001010001000000000', '00000001001000000000000000000000000001000000000000000', '00000001011000011110100000000000000000000000000000000', '00010001000000011110000100000000100000000000000000000', '10000000000000011110000000000000000110000000000000100', '01100010000000011000000000000000000101000000000000000', '01100011011000011010100000000000000100100000000000000', '01100010000000011000000000000000000101000001000000000', '01100010000000011000000000000000000100000000000100000', '00010000000000001110000000000000000000000000000000000', '00000000000000000010000100010000000100000000000000000', '01100000000000011000000000000000000100100000001000000', '00010001000000011110000100000000000000000000000010000', '01100010000000011010000100010000000100100000000000000', '10000001001000000000000000000000000110000000000000000', '00000000001000000011000000000000000000000000000000000', '00000000000000000010000100000000000000000000000000001', '00000000000000000010000100000000000100000000000000000', '00010000000000000010000000000000000000000000000001000', '00000010000000011000000000000000000001000001000000000', '10000000000000011010000100010000000010000000000000000', '00000001011000011110010100000000000000000000000000000', '00000001011000011100000000000000000001000000000000000', '00000001001000000000000000000001000001000001000000000', '00000001001000000000000000000000010000000000000000000', '00000001001000000010100000000000000100000000000000000', '00000000000000000010000100000000000000000000000000000', '10000000000000001110000000000000000110000000000000100', '00010000000000000000000000000000000000000000000000000', '00000000011000010010100000000000000000000000000000000', '00010011011000011110000000000000100100000000000000000', '01100010000000011010000100011000000100100000011000000', '10010000000000011110000100000000000110000000000000100', '10000001001000000010000000000000000110000000000000000', '00010000000001001100000000000000000001000011000000000', '00000000000000011100000000000000000001000001000000000'}
#106
codes_dict = {'01110010000000011000000000000000000000000000000000000': ['0', '79', '608', '730'], '00000000000000011110000100000000000000000000000000000': ['1', '8', '50', '219', '232', '245', '251', '283', '295', '299', '330', '349', '490', '495', '602', '611', '620', '785', '944', '1052', '1074', '1081', '1124', '1176', '1184'], '00000001001000000000000000000000000000000000000000000': ['2', '41', '75', '93', '198', '511', '545', '694', '848', '872', '907', '958', '1030'], '01100000000000011000000000000000000000000000000000000': ['3', '7', '15', '28', '36', '42', '61', '63', '68', '72', '78', '83', '84', '89', '91', '92', '95', '105', '112', '113', '122', '124', '128', '133', '139', '143', '145', '147', '151', '156', '158', '169', '172', '174', '178', '189', '194', '195', '204', '222', '224', '231', '242', '248', '253', '265', '271', '282', '284', '292', '296', '302', '303', '306', '309', '320', '323', '324', '328', '355', '361', '370', '373', '383', '384', '385', '391', '392', '393', '394', '395', '398', '402', '406', '419', '420', '426', '436', '451', '456', '461', '463', '466', '470', '473', '483', '485', '491', '496', '497', '510', '513', '514', '515', '518', '526', '527', '530', '543', '551', '556', '558', '560', '563', '565', '568', '575', '577', '581', '582', '583', '584', '586', '587', '591', '593', '599', '603', '604', '605', '607', '609', '610', '612', '619', '625', '631', '632', '637', '641', '643', '649', '666', '673', '675', '679', '681', '686', '696', '706', '707', '709', '715', '724', '725', '726', '729', '732', '735', '741', '743', '752', '755', '757', '763', '765', '766', '768', '769', '775', '789', '791', '811', '814', '821', '822', '834', '838', '844', '859', '864', '868', '884', '885', '887', '893', '896', '897', '901', '916', '928', '937', '946', '947', '948', '951', '954', '965', '970', '971', '972', '976', '989', '990', '998', '1002', '1008', '1016', '1027', '1033', '1042', '1057', '1066', '1073', '1079', '1086', '1091', '1093', '1096', '1112', '1114', '1118', '1119', '1122', '1129', '1134', '1136', '1147', '1150', '1154', '1161', '1163', '1165', '1173', '1174', '1187', '1189', '1198', '1204', '1206', '1209', '1211', '1212', '1217', '1228', '1237'], '01100010000000011010000100000000000100100000000000000': ['4', '38', '239', '304', '377', '573', '595', '767', '829', '831', '984', '1105', '1108'], '00000000000000000000000000000000000000000001000000000': ['9', '31', '46', '85', '97', '208', '252', '421', '440', '529', '550', '742', '770', '918', '1137', '1185', '1205', '1229'], '00000000000000000000000000000000000001000001000000000': ['10', '43', '54', '56', '73', '130', '160', '192', '196', '200', '202', '205', '212', '241', '256', '269', '287', '301', '318', '326', '331', '335', '353', '388', '397', '412', '442', '449', '467', '475', '478', '505', '532', '555', '564', '576', '579', '594', '596', '623', '627', '652', '698', '734', '738', '745', '764', '801', '802', '833', '843', '888', '931', '933', '975', '994', '1005', '1053', '1072', '1088', '1098', '1117', '1127', '1135', '1141', '1175', '1178', '1203', '1208', '1210', '1221'], '01100010000001011000000000000000000000000000000000000': ['13', '177'], '01100010000000011010000100000000000000000000000000000': ['14', '120', '264', '294', '325', '347', '382', '430', '539', '638', '664', '700', '701', '778', '818', '828', '930', '949', '1003', '1013', '1099', '1100', '1120', '1138', '1159', '1192', '1218', '1223'], '00000000000000000010000000000000000000000000000000000': ['16', '18', '25', '270', '368', '881', '925', '1021', '1039', '1156', '1213'], '00000000000000000010000100000000000000000000000000000': ['17', '90', '140', '144', '154', '289', '315', '322', '357', '366', '428', '443', '547', '653', '669', '689', '796', '800', '858', '898', '912', '926', '942', '956', '979', '1054', '1077', '1151', '1194', '1196'], '11110000100001011000000000000000000000000000000000000': ['20'], '00000000001000000000000000000000000000000000000000000': ['21', '55', '58', '59', '60', '65', '225', '233', '308', '312', '365', '525', '569', '601', '606', '654', '659', '670', '717', '798', '823', '826', '849', '876', '880', '892', '914', '929', '983', '1037', '1220', '1227'], '00000001000000000000000000000000000000000000000000000': ['23', '106', '188', '311', '378', '1040'], '00010000000000011100000000010000000000000000000000000': ['24'], '01100001010000011100000000000000000000000000000000000': ['26'], '00010000000000000010000100000000000000000000000000000': ['27', '69', '346', '574', '960', '969'], '10000000000000000000000000000000000000000000000000000': ['29', '70', '132', '138', '153', '230', '290', '327', '336', '351', '372', '380', '425', '459', '493', '494', '498', '501', '508', '520', '528', '540', '544', '553', '634', '695', '758', '773', '804', '806', '808', '817', '837', '842', '860', '867', '882', '889', '927', '940', '959', '964', '1014', '1022', '1094', '1115', '1139', '1170', '1190'], '00010000000000011010000010000000001100000000000000000': ['30'], '00000000000000001100000000000000000000000000000000000': ['32', '119', '123', '166', '180', '182', '227', '266', '344', '407', '448', '580', '585', '636', '640', '665', '672', '722', '731', '787', '788', '845', '851', '920', '961', '1010', '1012', '1017', '1046', '1084', '1092', '1107', '1128', '1164', '1202', '1216', '1235'], '10000001001000000000000000000000000110000000000000000': ['33', '522', '915', '1067'], '01100010000001011100000000000000000000000000000000000': ['34', '108', '812'], '00000000010000001000000000000000000000000000000000000': ['35', '369', '830'], '01100010000000011010000100010000000100100000000000000': ['37', '878', '1055'], '00000001001000000000000000000000000001000000000000000': ['39', '423'], '00010000000000000010000000000000000000000000000000000': ['40', '155', '203', '228', '235', '445', '644', '657', '728', '794', '857', '869', '910'], '10000000000000011110000100000000000110000000000000100': ['44', '111', '118', '135', '170', '171', '236', '321', '480', '507', '541', '571', '597', '703', '776', '906', '932', '955', '1001', '1009', '1044', '1049', '1082', '1132', '1207'], '10000000000000001110000000000000000000000000000000100': ['47', '1167'], '00010001010000001011000010000000000000000000000000000': ['48'], '00010001000000000010000000000000000000000000000000000': ['53', '432', '921'], '00010001000000011110000100000000100000000000000000000': ['64', '499', '835'], '01100000000000001000000000000000000000000000000000000': ['66', '207'], '10000000000000011010000100000000000010000000000000000': ['74', '648', '711', '852', '875', '1051', '1080', '1225'], '00010000000000001110000000000000000000000100000000000': ['77'], '00000000000001011010000100000000000000000000000000000': ['80'], '10000010000000011010000101010000000000000000000000000': ['81'], '00010000000001001100000000000000000001000011000000000': ['86'], '10000000000000001100000000000000000000000000000000100': ['87', '444', '453', '486', '727', '761', '779', '786', '861', '870', '890', '911', '1007', '1125', '1152', '1201'], '10000000000000011110000100000000000000000000000000100': ['94', '99', '101', '134', '210', '223', '243', '260', '288', '300', '329', '401', '460', '471', '535', '590', '629', '662', '687', '723', '736', '739', '747', '774', '805', '810', '813', '827', '895', '974', '988', '1018', '1063', '1078', '1097', '1104', '1111', '1121'], '00000100010100011000000000000000000000000000000000000': ['96', '250', '387', '403', '429', '502', '589', '656', '841'], '01100000000000011000000000000000000001000001100000000': ['98'], '10000000000000000010000100000000000000000000000000000': ['100', '109', '254', '367', '439', '487', '795', '941'], '01100010000000011110000100000000000000000000000000000': ['102', '168', '633', '1182'], '10000001001000000000000000000000000000000000000000000': ['104', '214', '272', '668', '820', '883', '966'], '00000010000000011010000100000000000000000000000000000': ['107', '237', '338', '446', '534', '613', '749', '1011', '1064'], '00000000011000001000000000000000000000000000000000000': ['114', '538', '1101'], '10000010000000011110000100000000000000000000000000100': ['115', '277'], '00010000000000001110000000000000000000000000000000000': ['116', '258', '358', '455', '782', '850', '991', '1140'], '00000001001000000010100000000000000100000000000000000': ['117'], '01100000000000011010000000000000000000000000000000000': ['121', '126', '137', '360', '476', '592', '899'], '10000001001000000000000001000000000000000000000000000': ['125'], '10000000100000000000000000000100000010000000000000000': ['127'], '01100011011000011010100000000000000100100000000000000': ['129', '1142'], '10000000100000000000000000000000000000000000000000000': ['131'], '10000001001000000010100000000000000000000000000000000': ['136'], '01100000000000011100000000000000000000000000000000000': ['141', '333', '375', '516', '533', '718', '824', '832', '963', '985', '1224'], '00000000000000000010000100010000000000000000000000000': ['142', '1083', '1197'], '00000000100000000010000100000000000000000000000000000': ['146'], '01100001010000101000000000000000000000000000000000000': ['148', '919'], '00000000000000000000000000000000000001000000000000000': ['149', '209', '909'], '00000001011000011110000000000000000001000000000000000': ['150'], '10000000000000000000000000000000000000000000000100000': ['157'], '00010000000000000000000000000000000000000000000000000': ['159', '399', '434'], '10000001010000011110010100000000000000000000000000100': ['161'], '00000000001100000000000000000000000000000000000000000': ['162', '762', '1026', '1219'], '00000001001000000000000000000001000001000001000000000': ['163', '191', '201', '274', '305', '417', '615', '737', '746', '982', '1019', '1062'], '00010000000000001110000000000000000100000000000010000': ['164'], '01100000000000011000000000000000000000000000100000000': ['167', '554', '630', '807', '865', '1133', '1191'], '01100001010000011000000000000000000000000000100000000': ['173'], '01100000000000001111000000000000000000000000000000000': ['175'], '01100010000000011000000000000000000000000000010000000': ['176'], '10000000000000011110000000000000000000000000000000000': ['179'], '01100010000000011000000000000000000000000000000000000': ['181', '340', '405', '441'], '00000000000000011000000000000000000000000000000000000': ['183', '342', '414', '1043'], '00000000000000000010000100000000000000000000000000001': ['184'], '00010000000000000010000100000000000000000001000000000': ['185', '379'], '01110000000000011000000000000000000000000000000000000': ['186'], '01100001010000011000000000000000000000000000000000000': ['190', '247', '278', '279', '350', '396', '978', '1157'], '00010001001000000000000000000001100001000001000000000': ['193'], '00000001000000000010000100000000010100000000000000000': ['197'], '00000000000000011010000100000000000000000000000000000': ['199', '206', '537', '559', '614'], '00000000001000000010000000000000000000000000000000000': ['211', '226', '792', '903', '1045', '1180'], '01111010000001011100000000000000000000000000000000000': ['213'], '01110010000000011000000010000000000101010001000000000': ['215'], '00000000000000001110000000000000000000000000000000000': ['218', '415', '437', '488', '719', '744', '784', '840', '1076'], '00000000000000000010000100000000000000000000000010000': ['220'], '00010000000000000010000000000000000000000000000001000': ['229'], '00000000000000011110000100000000000000000000000000010': ['238', '354', '624'], '01110000000001011100000000000000000001000001000000000': ['240'], '00000000000000000000000000000000000101000001000000000': ['244'], '10000000000000000000000001010000000000000000000000000': ['246', '1095'], '01110001010000011000000000000000100000000000100000000': ['249'], '00000101010000011000000000000000000000000000000000000': ['255', '362', '404'], '01100010000000011000000000000000000101000001100000000': ['257'], '00010000000000001100000000000000000000000000000000000': ['259'], '00000001010000001010000000000000000000000000000000000': ['261'], '00000000001100000010000000000000000000000000000000000': ['262'], '01100000000000011010000100000000000000000000000000000': ['263'], '10000000000000000010000101000000000000000000000000000': ['267', '500', '772', '1090'], '01110000000000001100000000000000000000000000000000000': ['268', '712'], '00000000000000000000000000000000000000010001000000000': ['273', '339'], '00000001010000011100000000000000000000000000010000000': ['275'], '00000000000000000010000100000000000100000000000000000': ['276', '297'], '00000001011000011100000000000000000001000000000000000': ['280', '411', '862'], '00000000000000000010000100000000000000000001000000000': ['281', '751', '825', '873'], '00000000000000000000000000010000000001000001000000000': ['285'], '00000000000000011100000000000000000000000000000000000': ['286', '923', '967', '1087', '1232'], '00000000000000000010000000000000000001010001000000000': ['291', '902', '1230'], '00010001000000001110000000000000000000000000000000000': ['293'], '00010001000000000000000000000000000000000000000000000': ['313', '431', '521', '1015'], '00000000000000000000000000010000000000000000000000000': ['314', '1103'], '00010001001000000000000000000000100000000000000000000': ['316'], '00010000011000000010000000000000000000000000000001000': ['317'], '00000000000000011110000100010000000000000000000000000': ['319', '519'], '00010000100001000000000000000000000000000000000000000': ['332'], '00010000000000000010000110000000000000000000000000000': ['334'], '00000001011000011110100000000000000000000000000000000': ['337', '647'], '00000000000000001000000000010000000000000000000000000': ['341', '1153'], '01100001010000011100000000000000000000000000100000000': ['343'], '10000000000000011010000100000000000000000000000000000': ['345', '381'], '00010000000000011110000100000000000000000000000000000': ['348', '424', '506', '777', '819', '1004', '1023'], '10000000100000011100000000000000000000000000000000000': ['352'], '01100010000000011100000000000000000000000000100000000': ['356'], '10010000000000000000000001010000000000000000000000000': ['363'], '00000001001000000000000000010001000001000001000000000': ['364'], '00000000000000000010000000000000000001000000000000000': ['371'], '00010001000010000010000000000000000000000000000000000': ['374'], '00000010000000001110000000000000000000000000000000000': ['386'], '00000001010000001000000000010000000000000000000000000': ['389'], '10000000000000000000000001000000000000000000000000000': ['410', '1214'], '00000001001000000000000001010000000000000000000000000': ['418'], '01100010000000011000000000000000000101000000000000000': ['435'], '10000000001000000010000000000000000000000000000000000': ['438', '924'], '00000001001000000000000000000000000000000001000000000': ['447', '816', '863'], '00000111010000011010000100000000000000000000000000000': ['450'], '01100010000000011110000100000000000100100000000000000': ['452', '1065'], '01100010000000011010000000000000000000000000000000000': ['454', '999', '1075'], '01100110010100011100000000000000000000000000000000000': ['457'], '10000000000000011010000100010000000010000000000000000': ['462'], '00000000000000001000000000000000000000000000000000000': ['464', '468', '552', '692'], '01100010000000011100000000000000000000000000000000000': ['465', '1186'], '01100000000000001100000000000000000000000000000000000': ['469'], '00000011011000011110010100000000000000000000000000000': ['472'], '10010000000000000010000000000000000000000000000000000': ['477', '682', '691'], '00000000000000000000000000000000000001000001000100000': ['479'], '10010000000000011110000100000000000110000000000000100': ['482'], '10010000000000011110000100000000000000000000000000100': ['484'], '10000000000000011110000100000000000000000000000000000': ['489', '720'], '00000000000000000010000101000000000000000000000000000': ['503'], '10000001011000011000000000000000000000000000000000000': ['504', '853', '952', '1068'], '00010001001010000000000000000000000000000000000000000': ['512'], '00000010000000011100000000000000000000000000000000000': ['517'], '00000000000000000000000001010000000000000000000000000': ['523'], '00000001001000000000000000010000000000000000000000000': ['524', '935'], '01100000000000001110000100000000000000000000000000000': ['536'], '00000001000000000010000100010000000000000000000010000': ['542'], '00010001010000011110100000000000000000000000000000000': ['546', '815', '1166'], '00000001000000011110000100000000000000000000010010000': ['548'], '01100010000000011000000000000000000100000000000100000': ['549'], '10000000000000000010000100000000000110000000000000000': ['557'], '01100000000000011000000000000000000100100000001000000': ['561', '635'], '01100010000000001110000000000000000000000000000000000': ['562'], '00010000001000000000000000000000000000000000000000000': ['566'], '10000000000000000010000000000000000010001000000000000': ['567'], '00000000000000000010000000000000000001000001000000000': ['570', '704', '854'], '01110000000000011110000100000000000000000000000000000': ['572'], '00010001001000000010000010000001100001010001000000000': ['578'], '11100000100000011000000000000000000000000000000000000': ['588'], '10000000000000000010000101011000000000000000000000000': ['598', '618'], '00000010000000011010000100000000000100000000000000000': ['600'], '10000001001000000000000001010000000000000000000000000': ['617', '995', '1038'], '00000001001000000010000000000000000001000000000000000': ['622'], '00000000000000000000000000000000000001000001010000000': ['628'], '01100010000000011010000100010000000000000000000000000': ['639'], '11100001011000001110000000000000000110000000000000100': ['646'], '10000000000000000010000001000000000000000000000000000': ['650'], '00000001011000011110010100000000000000000000000000000': ['651'], '10000000010000001000000000000000000000000000000000000': ['655'], '10000000000000000000000000000100000010000000000000000': ['660', '781'], '00000000001000000010100000000000000000000000000000001': ['661'], '00000001000000000010010100010000000000000000000000000': ['663'], '10000000000000011110000000000000000110000000000000100': ['667', '690'], '01100000000000011000000000000000000100100000000000000': ['671', '1109'], '01100011010000011010100000000000000000000000000000000': ['674', '839'], '01100011010000011000000000000000000000000000000000000': ['677', '683'], '00010001001000000000000000000000000000000000000000000': ['678'], '10000001000000000010000101000000000000000000000000000': ['684'], '10000000100000011100000000000000000000000000000000100': ['685'], '00010001011000011110100000000000000000000000000000000': ['688'], '11100000000001011100000000000000000000000000000000100': ['693'], '10000000000000000000000000010000000000000000000000000': ['697', '760'], '00000001010000001100000000000000000000000000000000000': ['699', '939', '973'], '01110000000000001110000000000000000000000000000000000': ['702'], '00010010000000011010000110000000000000000000000000000': ['705'], '00000001001000000010100000000000000000000000000000000': ['708'], '00000001001000000000000000000000010000000000000000000': ['710', '799'], '00000000001000000011000000000000000000000000000000000': ['713'], '10000001010000001100000000000000000000000000000000000': ['721'], '10010000000000000000000000000000000000000000000000000': ['733'], '10010001001000000010000000000100100010000000000000000': ['750'], '00010000001000000010000000000000000000000000000000000': ['753'], '00000000000000001110000000010000000000000000000000000': ['754', '874'], '00010000000000000000000000000000000000000001000000000': ['756'], '10000000001000000000000000000000000000000000000000000': ['759', '938'], '01100000000001011110000100000000000000000000000000000': ['790'], '10000001010000001100000000000000000000000000000000100': ['797', '957'], '00010001000000011110000100000000000000000000000010000': ['803', '846'], '01100001010000011010000000000000000000000000000000000': ['809', '1031', '1041'], '00000000011000001010000000000000000000000000000000000': ['836'], '00000001000000000010000100000000000000000000000000000': ['847'], '00010000000000001100000000010000000000000000000000000': ['855'], '01100010000000011010000100011000000100100000011000000': ['856'], '00000001000000001110000000000000000000000000000000000': ['866'], '00000000001000000000000000010000000000000000000000000': ['877'], '00000000000000000010000000000000000000000001000000000': ['879', '1144'], '00000011010000011100000000000000000000000000010000000': ['886'], '10000000000000000011000000000000000000000000000000000': ['891', '997'], '10000000000001001110000000000000000110000000000000100': ['894'], '00000000011000010010100000000000000000000000000000000': ['900'], '00000001001000000000000000000000000001000001000000000': ['904', '1172'], '00000001010000001110000000000000000000000000000000000': ['905', '1215'], '10000000000000001110000000000000000110000000000000100': ['908'], '00000000000000001010000000000000000000000000000000000': ['913'], '00000010000000001010000000000000000000000000000000000': ['922'], '10000001011000011110100000000000000000000000000000100': ['934', '981', '996'], '01100010000000011000000000000000000000000000100000000': ['936', '1233'], '01100010000001011100000000000000000000000000100000000': ['943'], '00010000000000000010000010000000001100000000000000000': ['945'], '10010001011000011000000000000000100000000000000000000': ['950'], '00010011011000011110000000000000100100000000000000000': ['953'], '00000000000000000010000100010000000100000000000000000': ['962', '1006'], '10010001000000000000000000000000000000000000000000000': ['968'], '01110000000000011110000010000000001100000000000000000': ['977'], '10000000000000001010000000000000000010000000000000000': ['986'], '00000001010000011100000000000000000000000000000000000': ['987'], '00000000000000011110000000000000000001000001000000000': ['992'], '00000000000000011100000000000000000001000001000000000': ['993'], '01100001010001011010000000000000000000000000000000000': ['1000'], '10000000000000011110000101010000000110000000000000100': ['1020'], '00000001001000000010000000010000000001000001000000000': ['1024'], '10000000000000000010000000000000000000000000000000000': ['1025'], '01100010000000011000000000000000000101000001000000000': ['1028'], '00010011011010011110000000000000000000000000000000000': ['1029'], '10000001001001000010100000000000000000000000000000000': ['1034'], '00010000000000000000000000010000000001000000000000000': ['1036'], '00000010000000011000000000000000000001000001000000000': ['1047'], '11100000000000011100000000000000000000000000000000100': ['1048', '1231'], '00010000000000000000001000000000000001000001000000000': ['1058'], '10000000000000011100000000000000000000000000000000100': ['1060', '1071'], '10000000000000011110000000000000000111000001000000100': ['1061'], '00000000000000001100000000000000000001000001000000000': ['1069'], '10000001001000000010000000000000000110000000000000000': ['1070'], '01100010000000011010000100000000000100000000000000000': ['1085'], '01100001011000011000000000000000000000000000000000000': ['1089'], '10000001010000001110000000000000000000000000000000100': ['1102'], '11100000000000011110000000000000000000000000000000100': ['1116'], '00010001010000001100000010000000000000000010000000000': ['1123'], '00000000000000000010000100011000000000000000000000000': ['1126'], '00000001000000000000000000010000000000000000000000000': ['1130'], '00000001011000011100000000000000000001000001000000000': ['1131'], '10011000000000001000000000000000000000000000000000000': ['1143'], '10000000000000000000000000000000000111000001000000000': ['1145'], '00000000100000000000000000000000000000000000000000000': ['1146'], '00000000001000000000000000000000000001000000000000000': ['1149'], '10010000000000001100000000000000000000000000000000100': ['1169'], '01100000000001011000000000000000000000000000100000000': ['1171'], '01100001010001010000000000000000000000000000000000000': ['1177'], '00010011011010011110000000000000001000000000000000000': ['1183'], '00000011010000001100000000000000000000000000000000000': ['1188'], '10000000000000011010000000000000000010000000000000000': ['1193'], '10000000001000000011000000000100000010000000000000000': ['1195'], '00000000000000001100000000010000000000000000000000000': ['1199'], '00010000000000011010000100000000000000000000000000000': ['1200'], '11100010000000011010000100000000000000000000000000000': ['1222'], '10000000000000000010000000000100000010000000000000000': ['1226'], '00010001010000001100000000000000000000000000000000000': ['1234'], '00000011010000011000000000000000000000000000000000000': ['1236']}
#277

def read():
    node = set()

    dir_list = os.listdir("../processed_file")
    for cur_file in dir_list:
        path = os.path.join("../processed_file", cur_file)
        #print(path)
        with open(path, "r", encoding="utf-8") as fp:
                for line in fp.readlines():
                    line = line.strip('\n')
                    if line == '?':
                        print(path)
                    node.add(line)
    return node




def resd_qes():
    with open('../data/train_qa.json', 'r', encoding='utf-8') as f:
        qa_data = json.loads(f.read())
    return qa_data


def test():
    P = QuestionPaser()
    dict = []
    qa_data = resd_qes()


    for key,index_list in codes_dict.items():
        print('key:', key)
        for index in index_list:
            q = qa_data[index]['question']
            result = P.parser(q)
            print(q)
            if result:
                print(q, "------------>", result)
                for i,j in result.items():
                    if i == 'code':
                        pass
                    print(i, end=' ')
                    for item in j:
                        print(item, end=' ')
                    print('\n')
            else:
                dict.append(key)
                print("\n", q, "\n")
        print('\n')
    print(dict)
    print(len(dict))



def tj():
    tj_dict = {}

    len_list = []
    #1-9, 11, 12, 13, 13, 13, 16, 18, 25, 25, 28, 30, 32, 37, 38, 49, 71, 236
    for index, value in codes_dict.items():
        length = len(value)
        tj_dict[index] = length
        len_list.append(length)
    len_list.sort()
    print(len_list)
    print(tj_dict)


#test()
tj()