import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random
import time

# -----------------------------
# STATE DATA
# -----------------------------
STATES = {
    "WA": {"name": "Washington", "initials": "WA", "capital": "Olympia"},
    "OR": {"name": "Oregon", "initials": "OR", "capital": "Salem"},
    "CA": {"name": "California", "initials": "CA", "capital": "Sacramento"},
    "AK": {"name": "Alaska", "initials": "AK", "capital": "Juneau"},
    "HI": {"name": "Hawaii", "initials": "HI", "capital": "Honolulu"},
    "ID": {"name": "Idaho", "initials": "ID", "capital": "Boise"},
    "NV": {"name": "Nevada", "initials": "NV", "capital": "Carson City"},
    "AZ": {"name": "Arizona", "initials": "AZ", "capital": "Phoenix"},
    "UT": {"name": "Utah", "initials": "UT", "capital": "Salt Lake City"},
    "MT": {"name": "Montana", "initials": "MT", "capital": "Helena"},
    "WY": {"name": "Wyoming", "initials": "WY", "capital": "Cheyenne"},
    "CO": {"name": "Colorado", "initials": "CO", "capital": "Denver"},
    "NM": {"name": "New Mexico", "initials": "NM", "capital": "Santa Fe"},
    "ND": {"name": "North Dakota", "initials": "ND", "capital": "Bismarck"},
    "SD": {"name": "South Dakota", "initials": "SD", "capital": "Pierre"},
    "NE": {"name": "Nebraska", "initials": "NE", "capital": "Lincoln"},
    "KS": {"name": "Kansas", "initials": "KS", "capital": "Topeka"},
    "OK": {"name": "Oklahoma", "initials": "OK", "capital": "Oklahoma City"},
    "TX": {"name": "Texas", "initials": "TX", "capital": "Austin"},
    "MN": {"name": "Minnesota", "initials": "MN", "capital": "Saint Paul"},
    "IA": {"name": "Iowa", "initials": "IA", "capital": "Des Moines"},
    "MO": {"name": "Missouri", "initials": "MO", "capital": "Jefferson City"},
    "AR": {"name": "Arkansas", "initials": "AR", "capital": "Little Rock"},
    "LA": {"name": "Louisiana", "initials": "LA", "capital": "Baton Rouge"},
    "WI": {"name": "Wisconsin", "initials": "WI", "capital": "Madison"},
    "IL": {"name": "Illinois", "initials": "IL", "capital": "Springfield"},
    "MS": {"name": "Mississippi", "initials": "MS", "capital": "Jackson"},
    "MI": {"name": "Michigan", "initials": "MI", "capital": "Lansing"},
    "IN": {"name": "Indiana", "initials": "IN", "capital": "Indianapolis"},
    "KY": {"name": "Kentucky", "initials": "KY", "capital": "Frankfort"},
    "TN": {"name": "Tennessee", "initials": "TN", "capital": "Nashville"},
    "AL": {"name": "Alabama", "initials": "AL", "capital": "Montgomery"},
    "OH": {"name": "Ohio", "initials": "OH", "capital": "Columbus"},
    "WV": {"name": "West Virginia", "initials": "WV", "capital": "Charleston"},
    "VA": {"name": "Virginia", "initials": "VA", "capital": "Richmond"},
    "NC": {"name": "North Carolina", "initials": "NC", "capital": "Raleigh"},
    "SC": {"name": "South Carolina", "initials": "SC", "capital": "Columbia"},
    "GA": {"name": "Georgia", "initials": "GA", "capital": "Atlanta"},
    "FL": {"name": "Florida", "initials": "FL", "capital": "Tallahassee"},
    "PA": {"name": "Pennsylvania", "initials": "PA", "capital": "Harrisburg"},
    "NY": {"name": "New York", "initials": "NY", "capital": "Albany"},
    "VT": {"name": "Vermont", "initials": "VT", "capital": "Montpelier"},
    "NH": {"name": "New Hampshire", "initials": "NH", "capital": "Concord"},
    "ME": {"name": "Maine", "initials": "ME", "capital": "Augusta"},
    "MA": {"name": "Massachusetts", "initials": "MA", "capital": "Boston"},
    "CT": {"name": "Connecticut", "initials": "CT", "capital": "Hartford"},
    "RI": {"name": "Rhode Island", "initials": "RI", "capital": "Providence"},
    "NJ": {"name": "New Jersey", "initials": "NJ", "capital": "Trenton"},
    "DE": {"name": "Delaware", "initials": "DE", "capital": "Dover"},
    "MD": {"name": "Maryland", "initials": "MD", "capital": "Annapolis"},
}

# -----------------------------
# REAL MAP BOUNDARIES
# -----------------------------
state_boundaries = {
    "Alabama": [(476, 280), (490, 279), (500, 279), (510, 280), (513, 295), (517, 307), (521, 318), (521, 326), (523, 339), (511, 341), (499, 342), (488, 342), (493, 352), (488, 353), (485, 348), (482, 352), (479, 352), (477, 337), (476, 318), (476, 306), (477, 291), (476, 280)],
    "Alaska": [(144, 400), (146, 469), (150, 468), (158, 474), (166, 472), (185, 500), (180, 503), (173, 491), (172, 495), (169, 490), (168, 484), (163, 483), (144, 473), (132, 469), (125, 463), (117, 463), (106, 463), (97, 472), (97, 478), (86, 484), (71, 492), (65, 491), (73, 483), (80, 476), (73, 469), (66, 468), (67, 462), (61, 460), (60, 455), (57, 446), (64, 436), (78, 438), (79, 427), (67, 424), (65, 419), (63, 414), (73, 412), (77, 413), (77, 417), (84, 416), (79, 408), (78, 404), (75, 399), (74, 395), (85, 394), (87, 388), (103, 384), (107, 385), (115, 391), (124, 393), (135, 397), (140, 396), (144, 400)],
    "Arizona": [(152, 233), (168, 235), (188, 238), (204, 240), (212, 241), (210, 259), (208, 283), (204, 301), (202, 313), (200, 328), (199, 331), (183, 328), (174, 326), (158, 317), (141, 307), (130, 301), (128, 298), (128, 296), (131, 295), (131, 291), (131, 287), (134, 283), (136, 280), (138, 277), (141, 274), (139, 267), (139, 264), (138, 258), (139, 252), (140, 246), (142, 243), (145, 246), (149, 244), (149, 240), (151, 233)],
    "Arkansas": [(393, 260), (444, 259), (450, 260), (447, 265), (454, 265), (449, 280), (446, 286), (446, 291), (442, 293), (437, 307), (439, 313), (400, 316), (401, 307), (395, 304), (393, 260)],
    "California": [(51, 126), (72, 132), (90, 137), (97, 140), (94, 156), (91, 164), (91, 171), (88, 180), (87, 186), (91, 192), (101, 207), (113, 225), (126, 244), (137, 259), (138, 268), (141, 274), (136, 277), (135, 281), (132, 285), (131, 290), (132, 294), (129, 296), (112, 295), (100, 293), (97, 284), (94, 276), (90, 272), (88, 272), (86, 266), (81, 266), (75, 258), (62, 251), (62, 245), (61, 240), (58, 231), (54, 222), (53, 217), (55, 212), (52, 209), (52, 201), (53, 197), (48, 191), (47, 184), (44, 177), (43, 170), (45, 165), (44, 156), (42, 149), (48, 140), (51, 126)],
    "Colorado": [(221, 180), (238, 181), (256, 183), (270, 185), (280, 186), (291, 187), (303, 189), (303, 202), (302, 214), (301, 229), (300, 240), (299, 250), (289, 251), (278, 249), (266, 248), (254, 247), (241, 245), (228, 243), (213, 242), (214, 230), (216, 218), (217, 208), (219, 196), (221, 180)],
    "Connecticut": [(636, 142), (653, 139), (656, 146), (637, 155), (636, 142)],
    "Delaware": [(629, 201), (623, 201), (617, 183), (619, 182), (625, 193), (629, 201)],
    "Florida": [(570, 338), (576, 350), (584, 363), (590, 370), (591, 376), (599, 389), (601, 404), (601, 413), (599, 420), (591, 420), (585, 414), (579, 409), (576, 405), (573, 399), (568, 398), (563, 389), (564, 383), (559, 382), (559, 371), (557, 365), (554, 364), (544, 356), (539, 352), (534, 354), (525, 358), (516, 354), (507, 350), (499, 350), (493, 349), (489, 342), (521, 339), (525, 343), (559, 342), (562, 344), (563, 336), (570, 338)],
    "Georgia": [(538, 274), (521, 275), (508, 278), (514, 298), (519, 313), (522, 316), (520, 321), (524, 338), (527, 344), (558, 342), (564, 344), (565, 336), (571, 337), (571, 327), (575, 316), (566, 301), (553, 291), (547, 284), (538, 280), (538, 274)],
    "Hawaii": [(224, 444), (221, 456), (233, 456), (236, 446), (224, 444), (252, 460), (255, 466), (262, 466), (258, 457), (252, 460), (272, 466), (269, 469), (278, 471), (278, 468), (273, 466), (287, 478), (294, 479), (292, 474), (287, 473), (282, 472), (282, 476), (287, 477), (298, 486), (296, 493), (294, 496), (296, 504), (298, 511), (304, 508), (312, 503), (316, 499), (311, 494), (306, 489), (298, 486)],
    "Idaho": [(155, 40), (164, 42), (164, 52), (165, 61), (166, 68), (171, 75), (173, 80), (176, 82), (175, 87), (173, 92), (172, 95), (174, 100), (179, 96), (179, 103), (181, 108), (183, 113), (186, 117), (190, 117), (195, 118), (201, 118), (203, 116), (205, 119), (205, 134), (203, 144), (200, 159), (184, 157), (167, 155), (150, 150), (139, 148), (133, 146), (134, 136), (136, 128), (138, 120), (140, 113), (138, 109), (142, 103), (148, 95), (150, 90), (147, 85), (145, 80), (149, 71), (152, 60), (153, 50), (155, 39)],
    "Iowa": [(372, 151), (428, 149), (433, 159), (438, 163), (442, 170), (440, 177), (434, 180), (435, 187), (429, 195), (379, 195), (377, 182), (370, 166), (372, 151)],
    "Illinois": [(439, 164), (468, 161), (476, 173), (478, 213), (478, 223), (473, 229), (473, 235), (472, 240), (467, 245), (459, 247), (457, 241), (445, 231), (446, 227), (447, 222), (440, 219), (432, 207), (428, 201), (428, 195), (434, 189), (435, 179), (441, 177), (443, 170), (439, 164)],
    "Indiana": [(476, 174), (483, 171), (496, 170), (506, 170), (511, 210), (511, 215), (507, 218), (498, 229), (494, 229), (493, 233), (487, 233), (475, 234), (476, 227), (479, 220), (478, 216), (476, 174)],
    "Kansas": [(303, 202), (320, 203), (336, 204), (352, 205), (365, 205), (383, 205), (388, 209), (386, 213), (392, 219), (392, 230), (392, 240), (392, 253), (376, 253), (357, 253), (338, 252), (321, 251), (310, 251), (300, 249), (301, 236), (301, 222), (302, 211), (302, 202)],
    "Kentucky": [(460, 257), (474, 257), (474, 254), (533, 249), (548, 233), (543, 227), (538, 218), (535, 213), (534, 218), (526, 217), (520, 215), (515, 211), (511, 211), (510, 216), (507, 218), (499, 229), (493, 230), (493, 233), (488, 233), (475, 235), (470, 242), (469, 247), (461, 247), (460, 257)],
    "Louisiana": [(403, 318), (438, 315), (441, 326), (436, 335), (435, 345), (454, 345), (458, 345), (462, 355), (456, 355), (419, 368), (412, 366), (405, 366), (406, 356), (408, 348), (405, 339), (402, 331), (403, 318)],
    "Maryland": [(573, 192), (615, 184), (616, 188), (611, 192), (612, 203), (614, 208), (603, 207), (604, 201), (597, 196), (590, 189), (587, 192), (580, 195), (575, 198), (573, 192)],
    "Massachusetts": [(636, 131), (643, 129), (653, 127), (661, 123), (662, 131), (670, 135), (677, 135), (669, 140), (665, 140), (658, 136), (637, 140), (636, 131)],
    "Maine": [(662, 118), (664, 106), (670, 102), (675, 99), (675, 94), (684, 88), (688, 86), (693, 80), (691, 74), (688, 74), (687, 70), (682, 67), (677, 52), (672, 46), (663, 48), (660, 46), (656, 53), (654, 68), (653, 78), (649, 85), (658, 115), (662, 118)],
    "Michigan": [(522, 167), (506, 171), (483, 171), (489, 159), (487, 149), (484, 140), (485, 128), (491, 120), (497, 114), (497, 108), (499, 104), (489, 103), (482, 107), (475, 108), (469, 117), (466, 108), (444, 102), (440, 98), (459, 84), (462, 86), (458, 92), (470, 95), (476, 99), (493, 92), (497, 96), (505, 96), (509, 101), (499, 103), (506, 108), (515, 112), (517, 121), (518, 126), (513, 133), (513, 138), (520, 136), (524, 132), (528, 137), (529, 150), (527, 155), (522, 167)],
    "Minnesota": [(363, 63), (382, 62), (384, 57), (387, 57), (389, 65), (399, 70), (405, 67), (415, 73), (425, 76), (430, 73), (440, 75), (419, 95), (415, 103), (413, 110), (409, 113), (412, 120), (413, 129), (429, 143), (428, 148), (371, 148), (371, 122), (367, 116), (370, 111), (366, 82), (363, 79), (363, 63)],
    "Mississippi": [(476, 281), (475, 313), (476, 334), (478, 351), (462, 355), (458, 345), (435, 344), (441, 326), (438, 315), (438, 308), (440, 298), (444, 291), (450, 281), (476, 281)],
    "Missouri": [(379, 196), (428, 195), (429, 202), (436, 210), (441, 217), (446, 222), (444, 229), (451, 235), (458, 244), (460, 248), (459, 255), (454, 264), (449, 264), (449, 257), (394, 259), (392, 219), (386, 212), (389, 208), (384, 204), (379, 196)],
    "Montana": [(166, 43), (197, 48), (232, 53), (260, 57), (290, 61), (287, 106), (284, 122), (209, 114), (204, 118), (188, 117), (182, 111), (179, 98), (174, 98), (176, 82), (170, 74), (165, 65), (165, 61), (163, 53), (166, 42), (166, 43)],
    "Nebraska": [(285, 155), (327, 157), (344, 156), (348, 159), (353, 159), (355, 162), (362, 162), (367, 164), (376, 183), (378, 195), (383, 204), (304, 202), (303, 188), (280, 184), (285, 155)],
    "Nevada": [(98, 140), (166, 155), (152, 233), (148, 247), (142, 244), (138, 260), (95, 197), (92, 192), (87, 186), (98, 140)],
    "New Mexico": [(213, 242), (250, 247), (287, 251), (284, 286), (282, 318), (281, 328), (234, 324), (234, 327), (214, 325), (213, 332), (200, 329), (213, 242)],
    "New Hampshire": [(649, 87), (658, 114), (662, 117), (661, 120), (655, 124), (644, 126), (642, 114), (643, 102), (646, 98), (644, 90), (649, 87)],
    "New Jersey": [(624, 155), (633, 159), (632, 165), (637, 174), (632, 191), (622, 186), (620, 182), (626, 174), (620, 167), (624, 155)],
    "New York": [(626, 96), (631, 117), (635, 129), (637, 140), (638, 153), (636, 158), (620, 153), (616, 148), (569, 156), (564, 156), (561, 154), (570, 144), (570, 137), (578, 133), (584, 133), (596, 129), (599, 124), (596, 117), (601, 110), (609, 100), (626, 96)],
    "North Carolina": [(624, 234), (609, 236), (597, 239), (586, 242), (574, 242), (563, 244), (550, 246), (550, 251), (548, 254), (542, 257), (537, 260), (533, 264), (529, 266), (524, 268), (522, 271), (522, 274), (537, 273), (547, 270), (553, 268), (560, 267), (567, 267), (570, 271), (583, 270), (600, 281), (607, 278), (609, 273), (617, 264), (623, 263), (626, 258), (622, 255), (621, 251), (625, 251), (629, 249), (629, 244), (623, 241), (628, 238), (624, 234)],
    "North Dakota": [(291, 61), (318, 62), (339, 63), (361, 63), (363, 80), (365, 84), (368, 110), (289, 109), (291, 61)],
    "Ohio": [(506, 170), (523, 167), (532, 172), (543, 167), (546, 163), (555, 159), (558, 183), (557, 195), (550, 201), (547, 209), (545, 209), (541, 216), (535, 214), (527, 216), (518, 212), (511, 211), (506, 170)],
    "Oklahoma": [(288, 251), (299, 250), (341, 252), (391, 253), (394, 261), (395, 271), (395, 282), (395, 293), (394, 304), (385, 303), (371, 303), (364, 303), (355, 301), (351, 302), (347, 298), (338, 297), (332, 293), (325, 290), (323, 261), (289, 259), (288, 251)],
    "Oregon": [(75, 62), (83, 68), (84, 76), (96, 77), (103, 80), (113, 79), (127, 81), (146, 84), (151, 91), (140, 105), (139, 110), (141, 114), (137, 119), (132, 145), (50, 125), (51, 113), (63, 90), (69, 73), (75, 62)],
    "Pennsylvania": [(562, 155), (565, 158), (615, 147), (621, 154), (620, 167), (627, 174), (621, 179), (615, 184), (591, 188), (562, 192), (560, 185), (555, 160), (562, 155)],
    "Rhode Island": [(656, 139), (657, 136), (663, 142), (657, 146), (656, 139)],
    "South Carolina": [(600, 280), (585, 270), (570, 271), (564, 267), (556, 268), (549, 268), (539, 273), (538, 278), (546, 284), (553, 291), (562, 299), (566, 304), (573, 314), (575, 314), (585, 303), (593, 295), (595, 287), (600, 280)],
    "South Dakota": [(288, 107), (367, 113), (365, 115), (370, 120), (372, 149), (368, 165), (362, 161), (356, 163), (347, 156), (284, 155), (287, 107)],
    "Tennessee": [(550, 247), (536, 248), (529, 250), (507, 252), (491, 253), (476, 253), (474, 256), (460, 256), (451, 276), (450, 281), (476, 280), (509, 279), (519, 275), (522, 269), (528, 265), (542, 257), (550, 247)],
    "Texas": [(289, 259), (325, 260), (324, 289), (329, 294), (334, 294), (339, 298), (346, 299), (352, 302), (358, 302), (367, 302), (372, 304), (381, 302), (388, 302), (394, 306), (400, 308), (400, 315), (401, 329), (406, 340), (408, 349), (406, 354), (406, 360), (404, 366), (398, 369), (392, 369), (389, 372), (387, 376), (383, 381), (375, 385), (370, 385), (367, 388), (363, 393), (359, 397), (356, 401), (355, 408), (354, 416), (356, 422), (357, 427), (350, 425), (335, 420), (328, 411), (326, 401), (314, 385), (308, 374), (302, 366), (293, 365), (285, 365), (280, 371), (277, 375), (265, 369), (257, 361), (254, 350), (234, 325), (280, 328), (289, 259)],
    "Utah": [(168, 155), (199, 160), (199, 175), (221, 179), (212, 240), (153, 231), (168, 155)],
    "Vermont": [(625, 95), (644, 91), (647, 99), (644, 102), (642, 117), (642, 127), (635, 130), (634, 121), (630, 117), (625, 95)],
    "Virginia": [(625, 233), (591, 241), (552, 246), (535, 245), (548, 233), (554, 235), (558, 233), (568, 228), (576, 212), (579, 212), (582, 205), (588, 195), (593, 195), (597, 196), (605, 200), (603, 206), (615, 210), (619, 221), (620, 227), (625, 227), (625, 233)],
    "Washington": [(98, 24), (154, 41), (146, 80), (146, 84), (124, 81), (110, 80), (101, 79), (84, 75), (83, 68), (74, 61), (76, 41), (74, 28), (95, 38), (93, 48), (99, 40), (98, 24)],
    "West Virginia": [(559, 187), (560, 194), (573, 193), (575, 197), (584, 194), (591, 191), (596, 194), (593, 196), (589, 196), (587, 200), (584, 203), (582, 207), (579, 211), (576, 210), (572, 215), (571, 223), (568, 227), (563, 232), (557, 234), (551, 234), (542, 227), (539, 219), (542, 213), (545, 209), (548, 203), (553, 201), (556, 197), (559, 187)],
    "Wisconsin": [(470, 161), (440, 163), (433, 159), (431, 150), (430, 148), (429, 144), (412, 129), (411, 118), (409, 113), (414, 108), (416, 98), (430, 94), (433, 98), (438, 98), (441, 102), (465, 110), (468, 118), (465, 127), (472, 124), (469, 136), (467, 149), (470, 161)],
    "Wyoming": [(210, 114), (238, 118), (260, 121), (284, 125), (283, 152), (281, 173), (280, 185), (232, 180), (220, 179), (202, 176), (199, 174), (198, 170), (200, 161), (202, 149), (206, 118), (210, 114)]
}

# -----------------------------
# CONFIG & RANKINGS
# -----------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RANKINGS_FILE = os.path.join(SCRIPT_DIR, "rankings.json")
if not os.access(SCRIPT_DIR, os.W_OK):
    RANKINGS_FILE = os.path.join(os.path.expanduser("~"), "rankings.json")
TIME_LIMIT = 300

# Modern Color Palette
COLORS = {
    "bg_dark": "#0F172A",      # Slate 900
    "bg_card": "#1E293B",      # Slate 800
    "accent": "#38BDF8",       # Sky 400
    "accent_hover": "#0EA5E9", # Sky 500
    "text_main": "#F8FAFC",    # Slate 50
    "text_dim": "#94A3B8",     # Slate 400
    "success": "#22C55E",      # Green 500
    "warning": "#F59E0B",      # Amber 500
    "danger": "#EF4444",       # Red 500
    "map_water": "#eaf4ff",    # Light Blue
    "map_land": "#8ecae6",     # Original Blue
    "map_highlight": "#ffb703",# Original Yellow
    "map_selected": "#90be6d"  # Original Green
}

def load_rankings():
    if os.path.exists(RANKINGS_FILE):
        try:
            with open(RANKINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_rankings(rankings):
    try:
        with open(RANKINGS_FILE, "w") as f:
            json.dump(rankings, f, indent=2)
    except OSError:
        fallback_file = os.path.join(os.path.expanduser("~"), "rankings.json")
        with open(fallback_file, "w") as f:
            json.dump(rankings, f, indent=2)

def insert_score(rankings, new_entry):
    rankings.append(new_entry)
    rankings.sort(key=lambda x: (-x["score"], x["elapsed"]))
    return rankings[:10]

# -----------------------------
# CUSTOM WIDGETS
# -----------------------------
class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        self.default_bg = kwargs.get("bg", COLORS["accent"])
        self.hover_bg = kwargs.get("activebackground", COLORS["accent_hover"])
        kwargs.setdefault("font", ("Helvetica", 11, "bold"))
        kwargs.setdefault("fg", COLORS["bg_dark"])
        kwargs.setdefault("bg", self.default_bg)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("padx", 20)
        kwargs.setdefault("pady", 10)
        kwargs.setdefault("cursor", "hand2")
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, e): self.config(bg=self.hover_bg)
    def on_leave(self, e): self.config(bg=self.default_bg)

class CardFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("bg", COLORS["bg_card"])
        kwargs.setdefault("padx", 20)
        kwargs.setdefault("pady", 20)
        super().__init__(master, **kwargs)

# -----------------------------
# MAIN APPLICATION
# -----------------------------
class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("US States Flashcards")
        self.attributes("-fullscreen", True)
        self.configure(bg=COLORS["bg_dark"])
        
        self.player_initials = ""
        self.score = 0.0
        self.elapsed = 0
        self.prompt_keys = []
        self.answer_keys = []
        self.deck = []
        self.current_index = 0
        self.timer_job = None
        self.start_time = None
        self.selected_map_answer = None
        self.answer_widgets = {}

        self.setup_styles()
        self.show_welcome()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar", thickness=10, troughcolor=COLORS["bg_card"], background=COLORS["accent"])

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def set_return_action(self, command):
        self.bind("<Return>", lambda e: command() if command else None)

    # -----------------------------
    # SCREENS
    # -----------------------------
    def show_welcome(self):
        self.clear_screen()
        self.set_return_action(self.handle_welcome_continue)
        
        container = tk.Frame(self, bg=COLORS["bg_dark"])
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="US STATES", font=("Georgia", 48, "bold"), bg=COLORS["bg_dark"], fg=COLORS["accent"]).pack()
        tk.Label(container, text="FLASHCARDS", font=("Helvetica", 18, "bold"), bg=COLORS["bg_dark"], fg=COLORS["text_dim"]).pack(pady=(0, 40))
        
        card = CardFrame(container)
        card.pack(pady=20)
        
        tk.Label(card, text="Enter Your Initials", font=("Helvetica", 12), bg=COLORS["bg_card"], fg=COLORS["text_main"]).pack(pady=(0, 10))
        self.initials_entry = tk.Entry(card, font=("Helvetica", 16), bg=COLORS["bg_dark"], fg=COLORS["text_main"], insertbackground=COLORS["text_main"], relief="flat", justify="center", width=10)
        self.initials_entry.pack(pady=10, ipady=8)
        self.initials_entry.focus_set()
        
        ModernButton(container, text="GET STARTED", command=self.handle_welcome_continue).pack(pady=30)

    def handle_welcome_continue(self):
        val = self.initials_entry.get().strip().upper()
        if not val:
            messagebox.showwarning("Initials", "Please enter your initials.")
            return
        self.player_initials = val[:3]
        self.show_instructions()

    def show_instructions(self):
        self.clear_screen()
        container = tk.Frame(self, bg=COLORS["bg_dark"])
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="How to Play", font=("Georgia", 32, "bold"), bg=COLORS["bg_dark"], fg=COLORS["text_main"]).pack(pady=(0, 30))
        card = CardFrame(container)
        card.pack()
        
        instructions = [
            "• Answer as many as possible in 300 seconds",
            "• Choose what to SHOW and what to ANSWER",
            "• Text answers earn 2x points over dropdowns",
            "• Click the map for 'Map Location' answers",
            "• Aim for the Top 10 leaderboard!"
        ]
        for text in instructions:
            tk.Label(card, text=text, font=("Helvetica", 12), bg=COLORS["bg_card"], fg=COLORS["text_dim"], anchor="w", justify="left").pack(fill="x", pady=5)
            
        ModernButton(container, text="CONTINUE TO SETTINGS", command=self.show_settings).pack(pady=40)

    def show_settings(self):
        self.clear_screen()
        self.set_return_action(self.validate_settings)
        
        header = tk.Frame(self, bg=COLORS["bg_dark"], pady=40)
        header.pack(fill="x")
        tk.Label(header, text="Quiz Settings", font=("Georgia", 32, "bold"), bg=COLORS["bg_dark"], fg=COLORS["text_main"]).pack()
        
        main_content = tk.Frame(self, bg=COLORS["bg_dark"])
        main_content.pack(expand=True)
        
        left_col = tk.Frame(main_content, bg=COLORS["bg_dark"], padx=20)
        left_col.pack(side="left", fill="y")
        
        show_card = CardFrame(left_col)
        show_card.pack(fill="x", pady=10)
        tk.Label(show_card, text="SHOW ON CARD", font=("Helvetica", 10, "bold"), bg=COLORS["bg_card"], fg=COLORS["accent"]).pack(anchor="w", pady=(0, 10))
        self.show_map = tk.BooleanVar(value=True); self.show_name = tk.BooleanVar(); self.show_initials = tk.BooleanVar(); self.show_capital = tk.BooleanVar()
        for label, var in [("Map Location", self.show_map), ("State Name", self.show_name), ("Initials", self.show_initials), ("Capital City", self.show_capital)]:
            tk.Checkbutton(show_card, text=label, variable=var, font=("Helvetica", 11), bg=COLORS["bg_card"], fg=COLORS["text_main"], selectcolor=COLORS["bg_dark"], activebackground=COLORS["bg_card"]).pack(anchor="w")

        ans_card = CardFrame(left_col)
        ans_card.pack(fill="x", pady=10)
        tk.Label(ans_card, text="USER ANSWERS", font=("Helvetica", 10, "bold"), bg=COLORS["bg_card"], fg=COLORS["accent"]).pack(anchor="w", pady=(0, 10))
        self.ans_map = tk.BooleanVar(); self.ans_name = tk.BooleanVar(value=True); self.ans_initials = tk.BooleanVar(); self.ans_capital = tk.BooleanVar()
        for label, var in [("Map Location", self.ans_map), ("State Name", self.ans_name), ("Initials", self.ans_initials), ("Capital City", self.ans_capital)]:
            tk.Checkbutton(ans_card, text=label, variable=var, font=("Helvetica", 11), bg=COLORS["bg_card"], fg=COLORS["text_main"], selectcolor=COLORS["bg_dark"], activebackground=COLORS["bg_card"]).pack(anchor="w")

        right_col = tk.Frame(main_content, bg=COLORS["bg_dark"], padx=20)
        right_col.pack(side="left", fill="y")
        mode_card = CardFrame(right_col)
        mode_card.pack(fill="x", pady=10)
        tk.Label(mode_card, text="ANSWER MODE", font=("Helvetica", 10, "bold"), bg=COLORS["bg_card"], fg=COLORS["accent"]).pack(anchor="w", pady=(0, 10))
        self.answer_mode = tk.StringVar(value="dropdown")
        for val, label in [("dropdown", "Multiple Choice (1pt)"), ("text", "Text Entry (2pts)")]:
            tk.Radiobutton(mode_card, text=label, variable=self.answer_mode, value=val, font=("Helvetica", 11), bg=COLORS["bg_card"], fg=COLORS["text_main"], selectcolor=COLORS["bg_dark"]).pack(anchor="w", pady=5)
            
        ModernButton(right_col, text="START QUIZ", command=self.validate_settings).pack(pady=20, fill="x")
        ModernButton(right_col, text="VIEW RANKINGS", bg=COLORS["bg_card"], activebackground=COLORS["bg_dark"], fg=COLORS["text_dim"], command=self.show_rankings).pack(fill="x")

    def validate_settings(self):
        p_keys = []; a_keys = []
        if self.show_map.get(): p_keys.append("map")
        if self.show_name.get(): p_keys.append("name")
        if self.show_initials.get(): p_keys.append("initials")
        if self.show_capital.get(): p_keys.append("capital")
        if self.ans_map.get(): a_keys.append("map")
        if self.ans_name.get(): a_keys.append("name")
        if self.ans_initials.get(): a_keys.append("initials")
        if self.ans_capital.get(): a_keys.append("capital")
        
        if not (1 <= len(p_keys) <= 3): messagebox.showwarning("Settings", "Select 1-3 items to SHOW."); return
        if not (1 <= len(a_keys) <= 3): messagebox.showwarning("Settings", "Select 1-3 items to ANSWER."); return
        if set(p_keys) & set(a_keys): messagebox.showwarning("Settings", "Shown and answered items cannot overlap."); return
        self.prompt_keys = p_keys; self.answer_keys = a_keys
        self.start_session()

    def start_session(self):
        self.score = 0.0; self.elapsed = 0; self.current_index = 0
        self.deck = list(STATES.keys()); random.shuffle(self.deck)
        self.start_time = time.time()
        if self.timer_job: self.after_cancel(self.timer_job)
        self.show_flashcard(); self.update_timer()

    def update_timer(self):
        self.elapsed = int(time.time() - self.start_time)
        time_left = max(0, TIME_LIMIT - self.elapsed)
        if hasattr(self, "timer_label"):
            self.timer_label.config(text=f"{time_left}s")
            self.progress['value'] = (time_left / TIME_LIMIT) * 100
        if time_left <= 0: self.finish_session(); return
        self.timer_job = self.after(1000, self.update_timer)

    def show_flashcard(self):
        self.clear_screen()
        self.answer_widgets = {}; self.selected_map_answer = None
        if self.current_index >= len(self.deck): self.finish_session(); return
        current_code = self.deck[self.current_index]; self.current_state = STATES[current_code]

        # Dashboard
        dash = tk.Frame(self, bg=COLORS["bg_card"], height=70); dash.pack(fill="x"); dash.pack_propagate(False)
        tk.Label(dash, text=f"PLAYER: {self.player_initials}", font=("Helvetica", 10, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack(side="left", padx=20)
        score_frame = tk.Frame(dash, bg=COLORS["bg_card"]); score_frame.pack(side="left", expand=True)
        tk.Label(score_frame, text="SCORE", font=("Helvetica", 8, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack()
        tk.Label(score_frame, text=f"{self.score:.2f}", font=("Helvetica", 14, "bold"), bg=COLORS["bg_card"], fg=COLORS["accent"]).pack()
        timer_frame = tk.Frame(dash, bg=COLORS["bg_card"]); timer_frame.pack(side="right", padx=20)
        tk.Label(timer_frame, text="TIME LEFT", font=("Helvetica", 8, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack()
        self.timer_label = tk.Label(timer_frame, text="300s", font=("Helvetica", 14, "bold"), bg=COLORS["bg_card"], fg=COLORS["warning"]); self.timer_label.pack()
        self.progress = ttk.Progressbar(self, style="TProgressbar", orient="horizontal", mode="determinate"); self.progress.pack(fill="x")

        # Content
        main_frame = tk.Frame(self, bg=COLORS["bg_dark"]); main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        left_frame = CardFrame(main_frame); left_frame.pack(side="left", fill="both", expand=True, padx=10)
        right_frame = CardFrame(main_frame); right_frame.pack(side="right", fill="y", padx=10)

        tk.Label(left_frame, text="Flashcard Prompt", font=("Georgia", 18, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_main"]).pack(pady=(0, 12))
        if "map" in self.prompt_keys or "map" in self.answer_keys:
            self.canvas = tk.Canvas(left_frame, width=760, height=560, bg=COLORS["map_water"], highlightthickness=0); self.canvas.pack(pady=10)
            self.draw_map(highlight_code=current_code if "map" in self.prompt_keys else None, show_labels=self.should_show_map_labels())
            if "map" in self.answer_keys: self.canvas.bind("<Button-1>", self.map_click)

        for key in ["name", "initials", "capital"]:
            if key in self.prompt_keys:
                tk.Label(left_frame, text=f"{key.capitalize()}: {self.current_state[key]}", font=("Helvetica", 13), bg=COLORS["bg_card"], fg=COLORS["text_main"]).pack(pady=6)

        tk.Label(right_frame, text="Your Answer", font=("Georgia", 18, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_main"]).pack(pady=(0, 12))
        for key in self.answer_keys:
            if key == "map":
                tk.Label(right_frame, text="Click the correct state on the map.", font=("Helvetica", 11), bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack(pady=6); continue
            tk.Label(right_frame, text=key.capitalize(), font=("Helvetica", 12, "bold"), bg=COLORS["bg_card"], fg=COLORS["accent"]).pack(pady=(10, 4))
            if self.answer_mode.get() == "text":
                entry = tk.Entry(right_frame, font=("Helvetica", 12), width=25, bg=COLORS["bg_dark"], fg=COLORS["text_main"], insertbackground=COLORS["text_main"], relief="flat"); entry.pack(pady=4, ipady=5); self.answer_widgets[key] = entry
            else:
                choices = self.make_choices(key, current_code); var = tk.StringVar(value=choices[0])
                menu = tk.OptionMenu(right_frame, var, *choices); menu.config(font=("Helvetica", 11), width=22, bg=COLORS["bg_dark"], fg=COLORS["text_main"], relief="flat"); menu.pack(pady=4); self.answer_widgets[key] = var

        if self.answer_mode.get() == "text": self.set_return_action(self.check_answer)
        btn_frame = tk.Frame(self, bg=COLORS["bg_dark"]); btn_frame.pack(pady=12)
        ModernButton(btn_frame, text="Submit Answer", command=self.check_answer).pack(side="left", padx=8)
        ModernButton(btn_frame, text="End Session", bg=COLORS["bg_card"], activebackground=COLORS["bg_dark"], fg=COLORS["text_dim"], command=self.finish_session).pack(side="left", padx=8)

    # -----------------------------
    # MAP LOGIC (Original)
    # -----------------------------
    def get_scaled_points(self, points, scale, x_offset, y_offset):
        return [(x * scale + x_offset, y * scale + y_offset) for x, y in points]

    def split_closed_polygons(self, points):
        polygons = []; current = []
        for point in points:
            current.append(point)
            if len(current) >= 4 and point == current[0]: polygons.append(current); current = []
        if len(current) >= 3: polygons.append(current)
        return polygons if polygons else [points]

    def point_in_polygon(self, x, y, points):
        inside = False; prev = len(points) - 1
        for curr in range(len(points)):
            cx, cy = points[curr]; px, py = points[prev]
            if ((cy > y) != (py > y)) and (x < (px - cx) * (y - cy) / (py - cy + 1e-9) + cx): inside = not inside
            prev = curr
        return inside

    def point_to_segment_distance_sq(self, px, py, x1, y1, x2, y2):
        dx = x2 - x1; dy = y2 - y1; l2 = dx*dx + dy*dy
        if l2 == 0: return (px-x1)**2 + (py-y1)**2
        t = max(0, min(1, ((px-x1)*dx + (py-y1)*dy) / l2))
        return (px - (x1 + t*dx))**2 + (py - (y1 + t*dy))**2

    def get_label_point(self, points):
        min_x = min(p[0] for p in points); max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points); max_y = max(p[1] for p in points)
        candidates = [(sum(p[0] for p in points)/len(points), sum(p[1] for p in points)/len(points))]
        step = max(2.0, min(max_x-min_x, max_y-min_y)/12.0)
        y = min_y
        while y <= max_y:
            x = min_x
            while x <= max_x:
                if self.point_in_polygon(x, y, points): candidates.append((x, y))
                x += step
            y += step
        best_x, best_y = (min_x+max_x)/2, (min_y+max_y)/2; best_score = -1.0
        for cx, cy in candidates:
            min_d = float('inf')
            for i in range(len(points)):
                d = self.point_to_segment_distance_sq(cx, cy, points[i][0], points[i][1], points[(i+1)%len(points)][0], points[(i+1)%len(points)][1])
                if d < min_d: min_d = d
            if min_d > best_score: best_score = min_d; best_x, best_y = cx, cy
        return best_x, best_y

    def should_show_map_labels(self): return not ("map" in self.prompt_keys and "initials" in self.answer_keys)

    def draw_map(self, highlight_code=None, selected_code=None, show_labels=True):
        self.canvas.delete("all"); self.state_items = {}; label_pts = {}
        m_l, m_t, m_r, m_b = 15, 15, 745, 545; m_w, m_h = m_r-m_l, m_b-m_t
        self.canvas.create_rectangle(m_l+3, m_t+3, m_r+3, m_b+3, fill="#d9e6f2", outline="", width=0)
        self.canvas.create_rectangle(m_l, m_t, m_r, m_b, fill="#f8fbff", outline="#c7d9ea", width=2)
        
        all_pts = []
        for info in STATES.values():
            if info["name"] in state_boundaries: all_pts.extend(state_boundaries[info["name"]])
        if not all_pts: return
        min_x, max_x = min(p[0] for p in all_pts), max(p[0] for p in all_pts)
        min_y, max_y = min(p[1] for p in all_pts), max(p[1] for p in all_pts)
        src_w, src_h = max_x-min_x, max_y-min_y; pad = 18
        scale = min((m_w-2*pad)/src_w, (m_h-2*pad)/src_h)
        off_x = m_l + (m_w - src_w*scale)/2 - min_x*scale
        off_y = m_t + (m_h - src_h*scale)/2 - min_y*scale

        for code, info in STATES.items():
            name = info["name"]
            if name not in state_boundaries: continue
            pts = self.get_scaled_points(state_boundaries[name], scale, off_x, off_y)
            fill = COLORS["map_land"]; outline = "#355070"
            if code == highlight_code: fill = COLORS["map_highlight"]; outline = "#d97706"
            if code == selected_code: fill = COLORS["map_selected"]; outline = "#2d6a4f"
            
            for poly_pts in self.split_closed_polygons(pts):
                flat = []; shadow = []
                for x, y in poly_pts: flat.extend([x, y]); shadow.extend([x+2, y+2])
                self.canvas.create_polygon(shadow, fill="#d9e6f2", outline="", smooth=False)
                p_id = self.canvas.create_polygon(flat, fill=fill, outline=outline, width=2.2, smooth=False, tags=("state", code))
                if code == highlight_code: self.canvas.create_polygon(flat, fill="", outline="red", width=3.2, smooth=False)
                self.state_items[p_id] = code

            cur_min_x = min(p[0] for p in pts); cur_max_x = max(p[0] for p in pts)
            cur_min_y = min(p[1] for p in pts); cur_max_y = max(p[1] for p in pts)
            w, h = cur_max_x-cur_min_x, cur_max_y-cur_min_y
            if show_labels and w >= 22 and h >= 14:
                cx, cy = self.get_label_point(pts); label_pts[code] = (cx, cy)
                f_s = 9 if w > 55 and h > 28 else 8
                self.canvas.create_text(cx+0.7, cy+0.7, text=code, font=("Arial", f_s, "bold"), fill="#f8fbff")
                self.canvas.create_text(cx, cy, text=code, font=("Arial", f_s, "bold"), fill="#0d1b2a")

        if show_labels:
            callouts = {"NH": (40, -18), "RI": (52, 6), "CT": (48, 20), "NJ": (42, 30), "DE": (38, 42)}
            for code, (dx, dy) in callouts.items():
                if code not in STATES: continue
                if code not in label_pts:
                    if STATES[code]["name"] not in state_boundaries: continue
                    pts = self.get_scaled_points(state_boundaries[STATES[code]["name"]], scale, off_x, off_y)
                    ax, ay = self.get_label_point(pts)
                else: ax, ay = label_pts[code]
                tx, ty = ax+dx, ay+dy; anchor = "w" if dx >= 0 else "e"; lx = tx-6 if dx >= 0 else tx+6
                self.canvas.create_line(ax, ay, lx, ty, fill="#1f3b5b", width=1.5)
                self.canvas.create_text(tx+0.7, ty+0.7, text=code, anchor=anchor, font=("Arial", 8, "bold"), fill="#f8fbff")
                self.canvas.create_text(tx, ty, text=code, anchor=anchor, font=("Arial", 8, "bold"), fill="#0d1b2a")

    def map_click(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag in STATES:
                    self.selected_map_answer = tag
                    self.draw_map(highlight_code=self.deck[self.current_index] if "map" in self.prompt_keys else None, selected_code=self.selected_map_answer, show_labels=self.should_show_map_labels())
                    return

    def make_choices(self, key, code):
        correct = STATES[code][key]
        others = [STATES[c][key] for c in STATES if STATES[c][key] != correct]
        choices = random.sample(others, 3) + [correct]
        random.shuffle(choices)
        return choices

    def check_answer(self):
        code = self.deck[self.current_index]; state = STATES[code]
        for key in self.answer_keys:
            if key == "map":
                if self.selected_map_answer == code: self.score += 1/6
                continue
            user_ans = self.answer_widgets[key].get().strip()
            pts = 2/6 if self.answer_mode.get() == "text" else 1/6
            if user_ans.lower() == state[key].lower(): self.score += pts
        self.current_index += 1; self.show_flashcard()

    def finish_session(self):
        if self.timer_job: self.after_cancel(self.timer_job); self.timer_job = None
        if self.start_time: self.elapsed = int(time.time() - self.start_time)
        rankings = load_rankings()
        rankings = insert_score(rankings, {"initials": self.player_initials, "elapsed": self.elapsed, "score": round(self.score, 2)})
        save_rankings(rankings); self.show_rankings()

    def show_rankings(self):
        self.clear_screen()
        container = tk.Frame(self, bg=COLORS["bg_dark"])
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Top 10 Rankings", font=("Georgia", 32, "bold"), bg=COLORS["bg_dark"], fg=COLORS["text_main"]).pack(pady=(0, 20))
        card = CardFrame(container); card.pack()
        
        headers = ["Rank", "Initials", "Time", "Score"]
        for col, h in enumerate(headers):
            tk.Label(card, text=h, font=("Helvetica", 12, "bold"), bg=COLORS["bg_card"], fg=COLORS["accent"], width=12).grid(row=0, column=col, padx=4, pady=4)
        
        rankings = load_rankings()
        for i, entry in enumerate(rankings, 1):
            tk.Label(card, text=str(i), font=("Helvetica", 11), bg=COLORS["bg_card"], fg=COLORS["text_dim"], width=12).grid(row=i, column=0, padx=4, pady=4)
            tk.Label(card, text=entry["initials"], font=("Helvetica", 11, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_main"], width=12).grid(row=i, column=1, padx=4, pady=4)
            tk.Label(card, text=f"{entry['elapsed']}s", font=("Helvetica", 11), bg=COLORS["bg_card"], fg=COLORS["text_dim"], width=12).grid(row=i, column=2, padx=4, pady=4)
            tk.Label(card, text=str(entry["score"]), font=("Helvetica", 11, "bold"), bg=COLORS["bg_card"], fg=COLORS["success"], width=12).grid(row=i, column=3, padx=4, pady=4)

        btn_frame = tk.Frame(container, bg=COLORS["bg_dark"]); btn_frame.pack(pady=30)
        ModernButton(btn_frame, text="PLAY AGAIN", command=self.show_settings).pack(side="left", padx=10)
        ModernButton(btn_frame, text="WELCOME SCREEN", bg=COLORS["bg_card"], activebackground=COLORS["bg_dark"], fg=COLORS["text_dim"], command=self.show_welcome).pack(side="left", padx=10)

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()
