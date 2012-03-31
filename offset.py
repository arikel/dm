#!/usr/bin/python
# -*- coding: utf-8 -*-

povOffsetDic = {}

povOffsetDic["02"] = (145, 95, 270, 186)
povOffsetDic["03"] = (183, 125, 194, 133)
povOffsetDic["13"] = (377, 125, 183, 133)
povOffsetDic["12"] = (415, 95, 145, 186)
povOffsetDic["12side"] = (377, 96, 38, 185)
povOffsetDic["10side"] = (505, 0, 55, 368)
povOffsetDic["11side"] = (415, 26, 90, 309)
povOffsetDic["01"] = (55, 25, 450, 310)
povOffsetDic["11"] = (505, 25, 55, 310)
povOffsetDic["23side"] = (505, 128, 55, 128)
povOffsetDic["13side"] = (355, 125, 22, 133)


for k, v in povOffsetDic.items():
	# building left version of facing and side tiles
	if int(k[0])!=0:
		newcode = "-" + k
		newx = 560-v[0]-v[2]
		povOffsetDic[newcode] = (newx, v[1], v[2], v[3])

povOffsetList = [
	"23side", "-23side", "13side", "-13side", "13", "-13", "03",
	"12side", "-12side", "12", "-12", "02", "11side", "-11side", "11", "-11", "01", "10side", "-10side"
]


itemOffsetDic = {}

itemOffsetDic["-24ul"] = (22,243)
itemOffsetDic["-24ur"] = (59,243)
itemOffsetDic["-24dl"] = (-5,246)
itemOffsetDic["-24dr"] = (17,246)
itemOffsetDic["24ul"] = (494,245)
itemOffsetDic["24ur"] = (541,245)
itemOffsetDic["24dl"] = (515,249)
itemOffsetDic["24dr"] = (550,249)
itemOffsetDic["-14ul"] = (101,247)
itemOffsetDic["-14ur"] = (151,246)
itemOffsetDic["-14dl"] = (84,250)
itemOffsetDic["-14dr"] = (141,250)
itemOffsetDic["14ul"] = (362, 246)
itemOffsetDic["14ur"] = (410, 246)
itemOffsetDic["14dl"] = (367,250)
itemOffsetDic["14dr"] = (432,250)
itemOffsetDic["04ul"] = (231, 246)
itemOffsetDic["04ur"] = (294,246)
itemOffsetDic["04dl"] = (222,249)
itemOffsetDic["04dr"] = (295,249)

itemOffsetDic["-23ul"] = ()
itemOffsetDic["-23ur"] = (-1,288)
itemOffsetDic["-23dl"] = ()
itemOffsetDic["-23dr"] = ()
itemOffsetDic["23ul"] = (541,258)
itemOffsetDic["23ur"] = ()
itemOffsetDic["23dl"] = ()
itemOffsetDic["23dr"] = ()
itemOffsetDic["-13ul"] = (57, 258)
itemOffsetDic["-13ur"] = (129,258)
itemOffsetDic["-13dl"] = (27,264)
itemOffsetDic["-13dr"] = (100,264)
itemOffsetDic["13ul"] = (375,258)
itemOffsetDic["13ur"] = (457,258)
itemOffsetDic["13dl"] = (384,264)
itemOffsetDic["13dr"] = (475,264)
itemOffsetDic["03ul"] = (213,258)
itemOffsetDic["03ur"] = (292,258)
itemOffsetDic["03dl"] = (199,265)
itemOffsetDic["03dr"] = (297,265)

itemOffsetDic["-12ul"] = (6,277)
itemOffsetDic["-12ur"] = (84,277)
itemOffsetDic["-12dl"] = (-5,288)
itemOffsetDic["-12dr"] = (61,288)
itemOffsetDic["12ul"] = (409,277)
itemOffsetDic["12ur"] = (513,277)
itemOffsetDic["12dl"] = (431,288)
itemOffsetDic["12dr"] = (522,288)
itemOffsetDic["02ul"] = (189,277)
itemOffsetDic["02ur"] = (290,277)
itemOffsetDic["02dl"] = (174,288)
itemOffsetDic["02dr"] = (300,288)

itemOffsetDic["-11ul"] = ()
itemOffsetDic["-11ur"] = (17,320)
itemOffsetDic["-11dl"] = ()
itemOffsetDic["-11dr"] = (-10,350)
itemOffsetDic["11ul"] = (477,320)
itemOffsetDic["11ur"] = ()
itemOffsetDic["11dl"] = (524,350)
itemOffsetDic["11dr"] = ()
itemOffsetDic["01ul"] = (147,320)
itemOffsetDic["01ur"] = (300,320)
itemOffsetDic["01dl"] = (112,350)
itemOffsetDic["01dr"] = (331,350)

itemOffsetDic["-10ul"] = ()
itemOffsetDic["-10ur"] = ()
itemOffsetDic["-10dl"] = ()
itemOffsetDic["-10dr"] = ()
itemOffsetDic["10ul"] = ()
itemOffsetDic["10ur"] = ()
itemOffsetDic["10dl"] = ()
itemOffsetDic["10dr"] = ()
itemOffsetDic["00ul"] = (60,395)
itemOffsetDic["00ur"] = (340,395)
itemOffsetDic["00dl"] = ()
itemOffsetDic["00dr"] = ()

itemOffsetList = itemOffsetDic.keys()
itemOffsetList.sort()
itemOffsetList.reverse()



