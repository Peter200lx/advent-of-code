import numpy as np

import re
from collections import namedtuple

DATA = """#1 @ 49,222: 19x20
#2 @ 162,876: 28x29
#3 @ 28,156: 17x18
#4 @ 673,337: 24x24
#5 @ 213,834: 20x23
#6 @ 675,523: 20x13
#7 @ 97,7: 11x27
#8 @ 92,512: 11x17
#9 @ 507,525: 27x20
#10 @ 47,742: 21x25
#11 @ 154,740: 28x25
#12 @ 808,793: 28x24
#13 @ 249,936: 13x11
#14 @ 93,400: 8x9
#15 @ 295,894: 17x22
#16 @ 535,885: 8x5
#17 @ 878,268: 13x11
#18 @ 152,685: 28x24
#19 @ 152,639: 22x26
#20 @ 905,560: 23x27
#21 @ 962,104: 19x12
#22 @ 125,145: 19x22
#23 @ 260,488: 13x21
#24 @ 179,815: 12x24
#25 @ 661,595: 4x6
#26 @ 584,97: 10x15
#27 @ 869,842: 11x19
#28 @ 491,825: 19x25
#29 @ 639,935: 10x28
#30 @ 583,26: 11x13
#31 @ 956,264: 22x17
#32 @ 168,706: 22x21
#33 @ 10,81: 29x18
#34 @ 751,214: 16x21
#35 @ 830,200: 17x20
#36 @ 587,580: 18x20
#37 @ 749,587: 10x13
#38 @ 546,376: 28x25
#39 @ 222,945: 11x28
#40 @ 43,937: 14x27
#41 @ 53,108: 25x21
#42 @ 669,894: 28x28
#43 @ 598,390: 23x25
#44 @ 440,136: 24x28
#45 @ 657,50: 16x13
#46 @ 134,155: 15x28
#47 @ 873,580: 28x16
#48 @ 519,287: 23x24
#49 @ 283,691: 12x20
#50 @ 78,660: 11x23
#51 @ 220,650: 24x21
#52 @ 722,671: 11x11
#53 @ 130,554: 12x26
#54 @ 248,423: 28x20
#55 @ 545,884: 10x3
#56 @ 926,657: 21x13
#57 @ 207,925: 22x27
#58 @ 813,292: 17x24
#59 @ 951,143: 23x25
#60 @ 582,397: 18x19
#61 @ 947,119: 14x24
#62 @ 874,701: 12x10
#63 @ 57,682: 10x18
#64 @ 450,510: 11x28
#65 @ 820,700: 27x17
#66 @ 231,114: 13x15
#67 @ 434,283: 22x18
#68 @ 489,743: 23x28
#69 @ 608,782: 10x24
#70 @ 297,896: 23x29
#71 @ 240,664: 13x29
#72 @ 96,953: 26x28
#73 @ 520,21: 21x25
#74 @ 878,207: 16x21
#75 @ 31,408: 19x26
#76 @ 846,419: 6x19
#77 @ 754,602: 17x29
#78 @ 95,621: 27x27
#79 @ 50,391: 10x24
#80 @ 915,362: 27x22
#81 @ 743,524: 25x23
#82 @ 41,58: 11x26
#83 @ 242,800: 27x21
#84 @ 525,652: 15x26
#85 @ 507,865: 18x26
#86 @ 855,272: 29x28
#87 @ 343,718: 12x13
#88 @ 405,628: 18x28
#89 @ 479,608: 20x13
#90 @ 752,934: 26x24
#91 @ 25,99: 14x12
#92 @ 909,952: 25x26
#93 @ 425,523: 27x12
#94 @ 345,586: 29x27
#95 @ 642,240: 16x10
#96 @ 369,567: 26x24
#97 @ 483,770: 23x10
#98 @ 745,683: 27x19
#99 @ 601,817: 16x21
#100 @ 793,153: 13x23
#101 @ 388,65: 15x20
#102 @ 66,971: 10x24
#103 @ 236,487: 25x21
#104 @ 661,56: 13x14
#105 @ 839,545: 16x16
#106 @ 215,222: 23x22
#107 @ 242,816: 26x23
#108 @ 213,402: 26x15
#109 @ 676,223: 21x22
#110 @ 297,445: 15x21
#111 @ 249,885: 27x28
#112 @ 300,213: 10x12
#113 @ 936,598: 22x11
#114 @ 755,384: 13x19
#115 @ 715,109: 15x11
#116 @ 636,97: 18x20
#117 @ 443,669: 27x19
#118 @ 710,106: 16x20
#119 @ 209,520: 16x28
#120 @ 26,770: 12x23
#121 @ 491,482: 12x11
#122 @ 949,666: 10x27
#123 @ 804,834: 13x22
#124 @ 959,831: 17x24
#125 @ 963,276: 11x25
#126 @ 822,113: 29x29
#127 @ 937,555: 28x25
#128 @ 350,576: 28x24
#129 @ 461,620: 29x20
#130 @ 964,42: 23x14
#131 @ 167,698: 20x19
#132 @ 61,130: 10x17
#133 @ 913,259: 20x22
#134 @ 444,359: 9x3
#135 @ 896,351: 20x17
#136 @ 763,331: 11x29
#137 @ 346,394: 28x22
#138 @ 901,51: 27x24
#139 @ 455,740: 27x10
#140 @ 244,491: 23x18
#141 @ 843,301: 24x13
#142 @ 437,908: 11x26
#143 @ 333,730: 27x10
#144 @ 706,121: 12x15
#145 @ 396,911: 12x28
#146 @ 750,275: 13x21
#147 @ 294,760: 21x20
#148 @ 339,787: 11x10
#149 @ 699,228: 14x29
#150 @ 813,609: 16x10
#151 @ 56,9: 18x22
#152 @ 886,882: 24x12
#153 @ 570,702: 11x24
#154 @ 692,588: 19x29
#155 @ 516,568: 12x27
#156 @ 939,720: 25x16
#157 @ 338,256: 13x11
#158 @ 586,373: 27x21
#159 @ 613,365: 28x18
#160 @ 765,412: 24x22
#161 @ 579,105: 11x27
#162 @ 286,788: 15x25
#163 @ 485,569: 23x11
#164 @ 891,562: 29x24
#165 @ 933,343: 21x21
#166 @ 963,832: 16x12
#167 @ 949,637: 27x27
#168 @ 918,374: 19x18
#169 @ 777,757: 17x21
#170 @ 720,97: 24x29
#171 @ 883,441: 6x19
#172 @ 749,790: 11x18
#173 @ 542,931: 13x23
#174 @ 590,779: 27x10
#175 @ 437,16: 19x11
#176 @ 688,883: 21x10
#177 @ 3,630: 21x21
#178 @ 943,128: 16x11
#179 @ 970,90: 13x14
#180 @ 816,501: 13x26
#181 @ 232,138: 25x16
#182 @ 356,500: 16x16
#183 @ 920,824: 12x17
#184 @ 116,442: 18x12
#185 @ 971,642: 11x25
#186 @ 508,187: 19x22
#187 @ 46,15: 24x27
#188 @ 958,121: 13x12
#189 @ 287,850: 18x21
#190 @ 564,326: 26x11
#191 @ 259,887: 24x29
#192 @ 306,578: 13x14
#193 @ 160,931: 29x13
#194 @ 518,70: 28x21
#195 @ 340,425: 29x15
#196 @ 512,663: 26x15
#197 @ 554,745: 19x25
#198 @ 473,636: 29x14
#199 @ 777,725: 8x3
#200 @ 187,140: 11x24
#201 @ 597,536: 11x14
#202 @ 721,111: 4x5
#203 @ 412,541: 10x14
#204 @ 739,927: 21x17
#205 @ 635,359: 25x20
#206 @ 163,522: 17x11
#207 @ 907,683: 15x21
#208 @ 453,361: 21x24
#209 @ 943,313: 25x22
#210 @ 117,966: 19x27
#211 @ 302,703: 19x15
#212 @ 897,123: 14x17
#213 @ 510,574: 11x10
#214 @ 529,578: 17x22
#215 @ 712,809: 15x15
#216 @ 236,599: 16x29
#217 @ 118,625: 29x18
#218 @ 768,198: 16x23
#219 @ 464,200: 29x15
#220 @ 131,389: 23x11
#221 @ 292,526: 18x10
#222 @ 148,953: 14x12
#223 @ 877,188: 18x26
#224 @ 704,107: 11x24
#225 @ 49,60: 18x17
#226 @ 245,675: 29x12
#227 @ 456,478: 29x18
#228 @ 256,470: 27x26
#229 @ 247,683: 17x10
#230 @ 174,509: 12x26
#231 @ 826,428: 25x21
#232 @ 434,717: 22x17
#233 @ 629,163: 13x10
#234 @ 84,660: 22x19
#235 @ 378,389: 18x16
#236 @ 683,31: 13x27
#237 @ 61,798: 29x12
#238 @ 21,506: 21x11
#239 @ 352,406: 12x10
#240 @ 602,643: 22x22
#241 @ 556,284: 13x11
#242 @ 319,470: 24x10
#243 @ 739,555: 17x29
#244 @ 670,20: 14x18
#245 @ 157,872: 27x21
#246 @ 226,847: 28x13
#247 @ 587,278: 14x27
#248 @ 656,207: 26x26
#249 @ 711,532: 17x19
#250 @ 239,434: 20x16
#251 @ 544,474: 23x13
#252 @ 385,486: 26x16
#253 @ 237,861: 10x6
#254 @ 644,710: 24x16
#255 @ 925,81: 28x11
#256 @ 26,759: 18x26
#257 @ 423,829: 24x18
#258 @ 114,578: 26x14
#259 @ 82,517: 22x18
#260 @ 747,108: 17x18
#261 @ 68,441: 15x18
#262 @ 717,679: 11x15
#263 @ 504,888: 21x15
#264 @ 908,120: 23x15
#265 @ 48,981: 29x10
#266 @ 238,493: 27x15
#267 @ 737,421: 29x13
#268 @ 901,898: 24x14
#269 @ 418,188: 18x19
#270 @ 585,662: 19x26
#271 @ 54,882: 27x10
#272 @ 535,743: 20x21
#273 @ 592,577: 24x25
#274 @ 170,768: 24x15
#275 @ 387,391: 26x26
#276 @ 304,854: 21x17
#277 @ 70,118: 24x15
#278 @ 581,408: 18x25
#279 @ 224,400: 13x19
#280 @ 26,345: 27x13
#281 @ 331,317: 13x26
#282 @ 221,353: 27x22
#283 @ 539,483: 16x16
#284 @ 397,67: 17x23
#285 @ 683,534: 22x29
#286 @ 159,256: 20x25
#287 @ 640,205: 14x17
#288 @ 479,489: 16x17
#289 @ 6,561: 16x28
#290 @ 586,443: 24x18
#291 @ 696,102: 13x12
#292 @ 429,390: 23x13
#293 @ 874,751: 28x14
#294 @ 825,114: 27x12
#295 @ 594,923: 20x24
#296 @ 593,248: 13x19
#297 @ 60,191: 18x11
#298 @ 630,525: 22x23
#299 @ 499,352: 10x13
#300 @ 578,678: 24x29
#301 @ 781,786: 10x24
#302 @ 156,730: 19x26
#303 @ 199,773: 26x10
#304 @ 159,191: 17x13
#305 @ 198,620: 11x13
#306 @ 956,710: 10x13
#307 @ 808,699: 23x10
#308 @ 913,259: 27x10
#309 @ 127,530: 14x29
#310 @ 703,629: 28x10
#311 @ 841,578: 22x15
#312 @ 361,73: 22x28
#313 @ 489,337: 20x28
#314 @ 13,601: 16x21
#315 @ 569,543: 28x10
#316 @ 321,469: 17x17
#317 @ 867,357: 27x23
#318 @ 215,241: 29x23
#319 @ 753,374: 24x17
#320 @ 75,945: 24x27
#321 @ 599,603: 10x15
#322 @ 712,83: 20x23
#323 @ 429,807: 14x19
#324 @ 376,675: 15x13
#325 @ 487,645: 28x22
#326 @ 298,92: 27x17
#327 @ 312,711: 26x22
#328 @ 602,547: 22x23
#329 @ 411,685: 14x23
#330 @ 865,551: 18x14
#331 @ 943,748: 21x25
#332 @ 113,322: 12x19
#333 @ 789,84: 21x29
#334 @ 264,920: 20x12
#335 @ 1,629: 25x10
#336 @ 983,23: 12x29
#337 @ 431,202: 28x26
#338 @ 720,143: 19x29
#339 @ 618,117: 23x10
#340 @ 60,133: 28x25
#341 @ 739,691: 14x15
#342 @ 654,353: 14x15
#343 @ 211,442: 17x19
#344 @ 417,651: 29x21
#345 @ 612,3: 21x17
#346 @ 427,393: 11x21
#347 @ 879,438: 20x27
#348 @ 314,842: 17x22
#349 @ 7,106: 26x14
#350 @ 351,68: 15x25
#351 @ 230,118: 16x17
#352 @ 440,283: 19x17
#353 @ 492,763: 21x24
#354 @ 696,875: 21x14
#355 @ 687,397: 12x12
#356 @ 498,727: 19x22
#357 @ 771,66: 23x24
#358 @ 72,683: 26x11
#359 @ 556,249: 22x17
#360 @ 628,354: 14x17
#361 @ 626,221: 24x27
#362 @ 732,914: 16x21
#363 @ 164,923: 14x15
#364 @ 924,738: 27x25
#365 @ 117,752: 15x21
#366 @ 619,368: 15x8
#367 @ 119,704: 20x16
#368 @ 187,775: 17x15
#369 @ 806,772: 19x27
#370 @ 567,697: 16x23
#371 @ 429,199: 10x15
#372 @ 402,600: 16x24
#373 @ 795,943: 19x19
#374 @ 755,802: 18x24
#375 @ 261,483: 10x17
#376 @ 840,80: 22x10
#377 @ 289,793: 3x10
#378 @ 701,818: 15x28
#379 @ 36,833: 13x10
#380 @ 45,50: 13x21
#381 @ 695,443: 17x11
#382 @ 141,338: 12x14
#383 @ 326,595: 21x23
#384 @ 597,52: 11x26
#385 @ 698,962: 29x27
#386 @ 898,419: 10x20
#387 @ 286,881: 28x19
#388 @ 288,515: 22x21
#389 @ 605,647: 24x26
#390 @ 438,223: 22x17
#391 @ 762,797: 22x20
#392 @ 256,469: 27x20
#393 @ 722,522: 20x23
#394 @ 315,436: 28x25
#395 @ 381,372: 25x20
#396 @ 290,695: 21x19
#397 @ 810,115: 21x18
#398 @ 467,744: 25x13
#399 @ 855,63: 26x24
#400 @ 499,149: 19x21
#401 @ 788,47: 24x29
#402 @ 303,578: 16x11
#403 @ 689,905: 12x19
#404 @ 894,65: 29x28
#405 @ 800,568: 23x14
#406 @ 881,146: 12x24
#407 @ 171,278: 18x12
#408 @ 645,845: 20x17
#409 @ 398,144: 23x13
#410 @ 592,537: 10x10
#411 @ 621,814: 14x12
#412 @ 544,919: 11x23
#413 @ 719,294: 12x19
#414 @ 724,112: 16x29
#415 @ 652,593: 28x14
#416 @ 930,660: 6x3
#417 @ 77,324: 23x19
#418 @ 153,187: 21x25
#419 @ 286,205: 16x19
#420 @ 865,287: 14x19
#421 @ 437,619: 29x16
#422 @ 162,852: 28x12
#423 @ 619,35: 11x15
#424 @ 314,707: 12x21
#425 @ 557,266: 19x25
#426 @ 196,449: 21x27
#427 @ 753,780: 16x23
#428 @ 86,662: 18x18
#429 @ 42,78: 29x11
#430 @ 859,739: 29x23
#431 @ 799,455: 20x15
#432 @ 38,353: 21x20
#433 @ 713,156: 27x13
#434 @ 743,214: 16x19
#435 @ 431,560: 29x14
#436 @ 329,533: 22x19
#437 @ 415,506: 28x24
#438 @ 333,779: 25x12
#439 @ 641,534: 17x19
#440 @ 780,481: 17x3
#441 @ 2,638: 26x25
#442 @ 572,875: 14x16
#443 @ 641,209: 12x12
#444 @ 60,160: 19x28
#445 @ 326,717: 18x17
#446 @ 436,925: 17x19
#447 @ 346,571: 25x16
#448 @ 635,467: 12x12
#449 @ 76,122: 19x13
#450 @ 29,57: 27x25
#451 @ 133,14: 27x28
#452 @ 429,121: 12x19
#453 @ 480,436: 14x28
#454 @ 675,666: 24x15
#455 @ 605,820: 26x22
#456 @ 16,755: 24x17
#457 @ 41,592: 15x14
#458 @ 318,478: 15x17
#459 @ 502,827: 25x17
#460 @ 217,476: 28x28
#461 @ 389,557: 19x18
#462 @ 777,829: 14x15
#463 @ 675,973: 10x16
#464 @ 78,890: 11x26
#465 @ 523,195: 20x22
#466 @ 309,964: 19x18
#467 @ 582,530: 10x25
#468 @ 717,548: 20x26
#469 @ 142,99: 6x10
#470 @ 697,593: 11x26
#471 @ 254,80: 23x12
#472 @ 779,761: 8x4
#473 @ 132,959: 22x24
#474 @ 806,582: 11x29
#475 @ 53,446: 12x14
#476 @ 92,359: 19x24
#477 @ 190,12: 23x28
#478 @ 690,523: 10x17
#479 @ 807,65: 20x13
#480 @ 958,108: 13x21
#481 @ 295,552: 22x28
#482 @ 951,634: 27x23
#483 @ 136,283: 26x20
#484 @ 375,126: 25x29
#485 @ 267,966: 24x23
#486 @ 563,637: 18x25
#487 @ 501,307: 28x11
#488 @ 944,68: 12x19
#489 @ 154,794: 11x21
#490 @ 558,305: 28x22
#491 @ 720,940: 16x26
#492 @ 768,812: 18x14
#493 @ 867,104: 23x23
#494 @ 127,270: 21x21
#495 @ 925,469: 11x24
#496 @ 861,554: 20x24
#497 @ 801,277: 28x18
#498 @ 346,117: 19x26
#499 @ 439,341: 25x25
#500 @ 708,843: 10x10
#501 @ 515,820: 18x25
#502 @ 579,523: 15x13
#503 @ 528,263: 28x12
#504 @ 54,369: 23x28
#505 @ 626,878: 23x27
#506 @ 597,803: 15x23
#507 @ 399,493: 21x16
#508 @ 511,449: 29x28
#509 @ 599,287: 11x15
#510 @ 921,337: 24x28
#511 @ 439,122: 23x20
#512 @ 180,221: 24x13
#513 @ 741,304: 24x11
#514 @ 967,835: 20x20
#515 @ 309,475: 16x28
#516 @ 422,830: 13x25
#517 @ 538,187: 28x10
#518 @ 976,201: 12x16
#519 @ 63,289: 28x10
#520 @ 556,632: 17x21
#521 @ 629,861: 20x24
#522 @ 369,186: 20x20
#523 @ 621,160: 14x19
#524 @ 505,167: 24x15
#525 @ 84,124: 25x16
#526 @ 776,839: 27x20
#527 @ 396,277: 21x29
#528 @ 776,232: 21x24
#529 @ 380,382: 16x20
#530 @ 959,914: 23x17
#531 @ 712,919: 17x13
#532 @ 932,59: 26x13
#533 @ 312,812: 21x17
#534 @ 188,260: 27x27
#535 @ 145,733: 18x13
#536 @ 919,571: 23x25
#537 @ 876,749: 29x13
#538 @ 699,929: 16x10
#539 @ 853,604: 10x11
#540 @ 336,444: 11x29
#541 @ 11,542: 29x19
#542 @ 561,971: 21x24
#543 @ 436,350: 29x19
#544 @ 857,588: 20x12
#545 @ 547,389: 15x20
#546 @ 658,178: 28x13
#547 @ 639,114: 12x17
#548 @ 128,746: 12x13
#549 @ 377,242: 23x13
#550 @ 382,158: 22x20
#551 @ 668,969: 11x25
#552 @ 467,181: 10x25
#553 @ 760,337: 29x20
#554 @ 674,210: 19x18
#555 @ 146,163: 15x25
#556 @ 126,320: 15x18
#557 @ 617,43: 12x27
#558 @ 170,746: 29x20
#559 @ 821,846: 17x27
#560 @ 710,18: 29x15
#561 @ 113,29: 22x26
#562 @ 116,22: 16x23
#563 @ 794,506: 13x27
#564 @ 402,0: 24x20
#565 @ 117,79: 25x21
#566 @ 682,670: 16x18
#567 @ 516,554: 13x17
#568 @ 935,468: 21x17
#569 @ 565,966: 24x28
#570 @ 41,834: 19x14
#571 @ 103,721: 26x25
#572 @ 651,18: 29x25
#573 @ 849,419: 23x25
#574 @ 940,700: 27x28
#575 @ 291,854: 21x12
#576 @ 23,536: 24x25
#577 @ 860,908: 27x12
#578 @ 48,186: 17x10
#579 @ 38,895: 24x27
#580 @ 630,886: 12x23
#581 @ 118,957: 25x14
#582 @ 530,205: 13x22
#583 @ 666,523: 13x15
#584 @ 966,172: 10x10
#585 @ 292,217: 24x19
#586 @ 426,688: 22x18
#587 @ 430,701: 12x16
#588 @ 398,510: 27x19
#589 @ 645,938: 15x26
#590 @ 526,334: 25x29
#591 @ 192,600: 21x10
#592 @ 178,675: 14x29
#593 @ 377,145: 25x11
#594 @ 733,566: 25x29
#595 @ 843,190: 21x23
#596 @ 261,823: 13x17
#597 @ 259,432: 21x26
#598 @ 344,914: 17x19
#599 @ 729,149: 12x16
#600 @ 745,287: 14x10
#601 @ 866,753: 29x28
#602 @ 753,793: 14x18
#603 @ 202,278: 20x17
#604 @ 643,572: 18x29
#605 @ 715,942: 16x15
#606 @ 360,402: 15x12
#607 @ 957,637: 21x14
#608 @ 916,656: 10x10
#609 @ 940,706: 20x10
#610 @ 217,474: 27x22
#611 @ 404,544: 11x14
#612 @ 452,89: 13x20
#613 @ 447,973: 22x25
#614 @ 959,272: 21x27
#615 @ 833,709: 25x25
#616 @ 770,202: 15x18
#617 @ 13,449: 16x25
#618 @ 735,644: 12x16
#619 @ 514,776: 15x17
#620 @ 929,504: 14x28
#621 @ 939,507: 13x22
#622 @ 681,539: 11x15
#623 @ 25,9: 29x18
#624 @ 595,544: 20x10
#625 @ 497,194: 12x12
#626 @ 250,945: 28x20
#627 @ 422,830: 11x13
#628 @ 964,655: 14x21
#629 @ 491,458: 15x13
#630 @ 977,733: 10x17
#631 @ 430,380: 28x21
#632 @ 76,298: 26x26
#633 @ 400,957: 29x21
#634 @ 500,880: 18x29
#635 @ 884,678: 12x21
#636 @ 20,162: 21x25
#637 @ 128,77: 14x15
#638 @ 925,596: 29x26
#639 @ 734,105: 29x24
#640 @ 70,445: 9x9
#641 @ 497,839: 22x19
#642 @ 263,940: 14x16
#643 @ 306,416: 23x16
#644 @ 715,177: 27x18
#645 @ 237,327: 12x18
#646 @ 36,408: 15x15
#647 @ 920,822: 15x23
#648 @ 130,817: 25x29
#649 @ 164,821: 22x22
#650 @ 743,471: 13x14
#651 @ 387,491: 17x16
#652 @ 282,646: 29x20
#653 @ 762,364: 28x19
#654 @ 465,349: 12x29
#655 @ 959,190: 21x15
#656 @ 643,547: 14x20
#657 @ 727,635: 10x13
#658 @ 155,501: 14x28
#659 @ 169,653: 15x26
#660 @ 483,478: 16x12
#661 @ 262,861: 15x28
#662 @ 852,333: 25x28
#663 @ 129,670: 18x22
#664 @ 691,849: 28x18
#665 @ 685,240: 28x26
#666 @ 560,688: 22x26
#667 @ 959,25: 13x19
#668 @ 153,754: 15x21
#669 @ 159,876: 12x15
#670 @ 396,74: 20x24
#671 @ 244,867: 24x26
#672 @ 620,157: 20x10
#673 @ 329,409: 21x24
#674 @ 591,75: 23x25
#675 @ 960,839: 23x12
#676 @ 283,88: 15x22
#677 @ 427,781: 15x21
#678 @ 595,295: 28x19
#679 @ 303,461: 16x12
#680 @ 855,582: 15x12
#681 @ 235,674: 21x13
#682 @ 888,178: 15x29
#683 @ 222,952: 26x26
#684 @ 879,902: 10x11
#685 @ 745,345: 24x22
#686 @ 915,197: 15x21
#687 @ 66,289: 28x10
#688 @ 133,915: 20x18
#689 @ 235,855: 15x25
#690 @ 686,377: 11x26
#691 @ 67,3: 25x13
#692 @ 170,660: 16x16
#693 @ 280,275: 23x24
#694 @ 284,859: 25x21
#695 @ 411,735: 20x23
#696 @ 762,597: 15x14
#697 @ 420,77: 10x26
#698 @ 743,512: 17x28
#699 @ 741,784: 23x26
#700 @ 174,131: 19x15
#701 @ 821,673: 27x19
#702 @ 830,970: 13x20
#703 @ 320,643: 25x17
#704 @ 218,521: 21x22
#705 @ 622,473: 21x14
#706 @ 552,326: 28x28
#707 @ 239,70: 26x10
#708 @ 444,626: 14x14
#709 @ 912,809: 27x18
#710 @ 772,764: 13x25
#711 @ 529,644: 21x26
#712 @ 564,391: 27x28
#713 @ 702,126: 16x20
#714 @ 317,937: 28x11
#715 @ 597,936: 13x24
#716 @ 732,536: 28x15
#717 @ 182,285: 22x15
#718 @ 963,397: 23x24
#719 @ 428,299: 18x17
#720 @ 798,348: 21x26
#721 @ 922,377: 23x11
#722 @ 336,246: 10x24
#723 @ 708,668: 10x21
#724 @ 827,296: 27x17
#725 @ 134,970: 21x29
#726 @ 2,21: 20x20
#727 @ 177,216: 15x18
#728 @ 789,926: 15x28
#729 @ 728,452: 27x25
#730 @ 817,303: 25x10
#731 @ 857,421: 29x25
#732 @ 293,879: 10x27
#733 @ 8,746: 28x20
#734 @ 148,518: 16x18
#735 @ 835,435: 10x13
#736 @ 80,798: 24x12
#737 @ 88,29: 17x26
#738 @ 981,77: 17x12
#739 @ 179,890: 20x26
#740 @ 565,851: 15x23
#741 @ 512,786: 13x11
#742 @ 595,828: 24x10
#743 @ 272,54: 15x29
#744 @ 452,120: 23x12
#745 @ 387,526: 28x15
#746 @ 966,43: 28x29
#747 @ 176,197: 10x22
#748 @ 477,959: 21x29
#749 @ 199,19: 27x12
#750 @ 404,619: 13x17
#751 @ 811,681: 23x13
#752 @ 395,163: 11x28
#753 @ 133,272: 29x28
#754 @ 404,618: 18x24
#755 @ 387,294: 12x16
#756 @ 88,946: 24x11
#757 @ 132,729: 27x21
#758 @ 73,132: 24x29
#759 @ 958,234: 10x18
#760 @ 508,824: 27x11
#761 @ 910,357: 13x17
#762 @ 887,674: 22x21
#763 @ 896,579: 10x23
#764 @ 451,565: 16x23
#765 @ 440,702: 10x11
#766 @ 446,363: 18x21
#767 @ 631,87: 27x16
#768 @ 888,900: 21x23
#769 @ 395,638: 15x25
#770 @ 104,964: 18x11
#771 @ 808,407: 24x16
#772 @ 552,169: 10x22
#773 @ 525,874: 10x12
#774 @ 422,220: 16x14
#775 @ 317,742: 23x18
#776 @ 509,111: 27x10
#777 @ 590,29: 13x11
#778 @ 515,21: 20x15
#779 @ 962,624: 13x21
#780 @ 449,409: 29x25
#781 @ 754,967: 17x14
#782 @ 45,545: 23x23
#783 @ 816,833: 18x11
#784 @ 932,633: 22x25
#785 @ 785,345: 21x10
#786 @ 931,755: 28x17
#787 @ 126,92: 28x10
#788 @ 644,226: 19x28
#789 @ 172,612: 29x18
#790 @ 789,163: 19x14
#791 @ 828,417: 10x18
#792 @ 703,662: 10x11
#793 @ 971,7: 17x22
#794 @ 149,71: 12x24
#795 @ 64,50: 12x27
#796 @ 127,16: 20x25
#797 @ 330,614: 19x16
#798 @ 545,659: 27x20
#799 @ 55,121: 25x13
#800 @ 198,533: 28x26
#801 @ 261,557: 27x11
#802 @ 303,107: 10x19
#803 @ 558,939: 24x15
#804 @ 287,830: 29x28
#805 @ 904,864: 15x29
#806 @ 471,769: 25x29
#807 @ 838,589: 29x25
#808 @ 945,304: 25x20
#809 @ 623,173: 28x20
#810 @ 803,448: 14x10
#811 @ 132,321: 21x22
#812 @ 244,918: 25x24
#813 @ 127,326: 22x26
#814 @ 179,495: 10x16
#815 @ 160,873: 24x19
#816 @ 558,93: 25x17
#817 @ 326,700: 26x26
#818 @ 165,779: 13x21
#819 @ 109,437: 24x25
#820 @ 17,58: 27x19
#821 @ 889,101: 12x19
#822 @ 319,171: 27x25
#823 @ 51,960: 16x17
#824 @ 955,544: 26x20
#825 @ 976,71: 15x19
#826 @ 954,379: 26x26
#827 @ 516,361: 11x10
#828 @ 512,521: 18x28
#829 @ 676,263: 27x23
#830 @ 825,386: 11x14
#831 @ 253,654: 15x12
#832 @ 318,459: 20x15
#833 @ 940,309: 29x16
#834 @ 951,310: 18x26
#835 @ 496,942: 22x28
#836 @ 355,821: 19x26
#837 @ 443,396: 21x12
#838 @ 958,141: 15x27
#839 @ 849,913: 27x20
#840 @ 2,445: 18x27
#841 @ 722,129: 21x23
#842 @ 874,64: 15x25
#843 @ 872,607: 26x19
#844 @ 846,591: 23x23
#845 @ 500,823: 28x11
#846 @ 864,847: 19x24
#847 @ 257,48: 16x23
#848 @ 497,772: 28x12
#849 @ 601,611: 10x23
#850 @ 624,348: 20x24
#851 @ 284,285: 9x10
#852 @ 684,875: 25x20
#853 @ 279,426: 28x11
#854 @ 777,236: 11x19
#855 @ 117,740: 10x17
#856 @ 262,886: 27x13
#857 @ 37,587: 19x25
#858 @ 237,537: 28x16
#859 @ 329,302: 25x17
#860 @ 312,7: 23x22
#861 @ 741,93: 18x29
#862 @ 228,887: 18x12
#863 @ 77,962: 20x15
#864 @ 531,878: 17x22
#865 @ 131,385: 20x12
#866 @ 148,955: 15x23
#867 @ 653,698: 27x27
#868 @ 188,121: 23x17
#869 @ 310,288: 22x14
#870 @ 749,461: 14x29
#871 @ 307,713: 12x29
#872 @ 409,719: 24x28
#873 @ 291,650: 22x16
#874 @ 643,560: 26x21
#875 @ 20,3: 16x26
#876 @ 709,447: 10x11
#877 @ 821,223: 13x16
#878 @ 516,740: 18x20
#879 @ 66,222: 3x5
#880 @ 108,532: 20x17
#881 @ 447,73: 22x11
#882 @ 121,289: 20x11
#883 @ 44,753: 20x12
#884 @ 90,677: 20x15
#885 @ 718,179: 13x18
#886 @ 830,700: 25x13
#887 @ 288,317: 26x12
#888 @ 117,700: 25x25
#889 @ 306,743: 24x10
#890 @ 744,966: 18x14
#891 @ 530,665: 21x10
#892 @ 743,657: 11x10
#893 @ 244,959: 12x22
#894 @ 748,130: 22x11
#895 @ 657,827: 24x10
#896 @ 194,607: 29x15
#897 @ 861,598: 17x14
#898 @ 843,735: 14x18
#899 @ 64,121: 26x29
#900 @ 843,588: 13x21
#901 @ 755,225: 26x12
#902 @ 612,339: 25x22
#903 @ 588,98: 27x10
#904 @ 309,583: 27x17
#905 @ 508,807: 22x27
#906 @ 221,618: 11x16
#907 @ 590,510: 23x28
#908 @ 825,794: 22x28
#909 @ 87,397: 27x16
#910 @ 389,346: 12x27
#911 @ 200,623: 5x3
#912 @ 265,313: 26x24
#913 @ 264,935: 16x29
#914 @ 612,905: 20x13
#915 @ 498,745: 29x12
#916 @ 766,198: 10x29
#917 @ 410,941: 24x17
#918 @ 399,97: 14x15
#919 @ 287,863: 19x27
#920 @ 550,651: 27x28
#921 @ 354,915: 28x21
#922 @ 409,600: 17x21
#923 @ 348,813: 28x15
#924 @ 983,796: 15x21
#925 @ 137,707: 22x10
#926 @ 400,950: 29x14
#927 @ 183,681: 23x24
#928 @ 565,245: 25x28
#929 @ 286,79: 29x25
#930 @ 956,553: 18x19
#931 @ 850,419: 18x12
#932 @ 694,1: 18x19
#933 @ 753,429: 16x12
#934 @ 309,976: 14x10
#935 @ 405,183: 13x13
#936 @ 855,598: 28x14
#937 @ 40,439: 24x19
#938 @ 591,551: 21x17
#939 @ 398,100: 29x24
#940 @ 413,711: 28x17
#941 @ 62,285: 23x27
#942 @ 737,342: 29x28
#943 @ 22,612: 16x15
#944 @ 822,418: 12x18
#945 @ 51,51: 10x22
#946 @ 542,249: 11x24
#947 @ 664,23: 24x20
#948 @ 366,66: 25x27
#949 @ 227,829: 12x15
#950 @ 160,655: 24x25
#951 @ 412,147: 13x10
#952 @ 814,406: 24x21
#953 @ 941,919: 25x20
#954 @ 858,407: 14x21
#955 @ 291,869: 10x15
#956 @ 844,417: 11x24
#957 @ 169,836: 16x20
#958 @ 447,12: 13x12
#959 @ 306,773: 12x27
#960 @ 291,851: 27x11
#961 @ 414,803: 11x22
#962 @ 427,760: 24x22
#963 @ 647,10: 11x28
#964 @ 860,581: 24x18
#965 @ 616,8: 19x20
#966 @ 286,422: 24x10
#967 @ 889,551: 16x14
#968 @ 302,568: 16x25
#969 @ 232,83: 27x25
#970 @ 720,543: 24x21
#971 @ 322,317: 14x23
#972 @ 180,731: 25x28
#973 @ 361,131: 27x13
#974 @ 345,616: 15x24
#975 @ 597,43: 26x17
#976 @ 946,260: 26x15
#977 @ 646,831: 18x14
#978 @ 96,810: 11x11
#979 @ 840,973: 10x17
#980 @ 133,821: 16x18
#981 @ 728,398: 15x27
#982 @ 835,562: 12x25
#983 @ 877,789: 10x20
#984 @ 417,136: 16x24
#985 @ 600,822: 16x11
#986 @ 825,405: 25x15
#987 @ 20,507: 28x22
#988 @ 923,646: 27x20
#989 @ 43,68: 26x22
#990 @ 241,661: 29x17
#991 @ 772,445: 19x15
#992 @ 925,940: 18x27
#993 @ 251,615: 21x20
#994 @ 814,719: 12x29
#995 @ 43,141: 26x12
#996 @ 129,278: 20x17
#997 @ 266,925: 17x23
#998 @ 171,475: 10x25
#999 @ 641,534: 29x12
#1000 @ 972,48: 25x17
#1001 @ 806,913: 15x14
#1002 @ 770,952: 13x11
#1003 @ 554,841: 18x18
#1004 @ 36,37: 14x11
#1005 @ 414,620: 15x17
#1006 @ 638,223: 18x27
#1007 @ 374,674: 13x15
#1008 @ 921,650: 19x17
#1009 @ 507,746: 28x28
#1010 @ 782,456: 11x26
#1011 @ 329,386: 22x20
#1012 @ 579,932: 18x25
#1013 @ 404,833: 28x15
#1014 @ 157,102: 24x17
#1015 @ 653,209: 14x29
#1016 @ 318,98: 27x11
#1017 @ 507,495: 25x29
#1018 @ 803,745: 19x19
#1019 @ 731,94: 15x21
#1020 @ 198,629: 21x28
#1021 @ 587,656: 23x19
#1022 @ 44,912: 28x21
#1023 @ 0,631: 25x12
#1024 @ 47,375: 22x14
#1025 @ 934,124: 25x16
#1026 @ 674,11: 21x21
#1027 @ 300,823: 28x24
#1028 @ 380,406: 18x27
#1029 @ 917,381: 21x22
#1030 @ 717,646: 26x10
#1031 @ 112,737: 26x11
#1032 @ 928,544: 27x23
#1033 @ 353,597: 14x3
#1034 @ 87,324: 28x18
#1035 @ 292,656: 28x17
#1036 @ 970,269: 16x22
#1037 @ 89,324: 15x16
#1038 @ 540,876: 19x20
#1039 @ 754,812: 24x26
#1040 @ 819,32: 16x23
#1041 @ 775,720: 13x21
#1042 @ 929,69: 11x24
#1043 @ 911,45: 19x17
#1044 @ 577,665: 21x11
#1045 @ 115,27: 13x10
#1046 @ 396,739: 25x27
#1047 @ 502,874: 14x21
#1048 @ 956,364: 17x22
#1049 @ 316,524: 24x22
#1050 @ 895,903: 21x12
#1051 @ 566,884: 29x16
#1052 @ 186,749: 19x24
#1053 @ 630,536: 18x21
#1054 @ 161,753: 14x13
#1055 @ 239,935: 13x17
#1056 @ 62,764: 12x16
#1057 @ 399,617: 20x22
#1058 @ 867,433: 10x10
#1059 @ 229,544: 17x14
#1060 @ 666,391: 27x19
#1061 @ 228,480: 10x29
#1062 @ 801,561: 21x13
#1063 @ 62,218: 13x15
#1064 @ 804,506: 16x24
#1065 @ 31,726: 26x25
#1066 @ 813,872: 22x14
#1067 @ 883,913: 21x18
#1068 @ 930,270: 28x10
#1069 @ 453,398: 24x16
#1070 @ 289,404: 26x15
#1071 @ 432,749: 25x11
#1072 @ 601,51: 10x10
#1073 @ 726,934: 10x28
#1074 @ 77,648: 16x16
#1075 @ 684,623: 26x10
#1076 @ 501,811: 10x16
#1077 @ 749,865: 15x14
#1078 @ 432,721: 20x25
#1079 @ 623,818: 10x15
#1080 @ 431,843: 10x11
#1081 @ 430,807: 25x13
#1082 @ 707,290: 25x10
#1083 @ 906,806: 23x13
#1084 @ 946,351: 12x25
#1085 @ 882,202: 16x14
#1086 @ 950,626: 24x13
#1087 @ 189,721: 14x13
#1088 @ 816,674: 16x18
#1089 @ 877,580: 24x24
#1090 @ 215,531: 20x18
#1091 @ 670,873: 23x13
#1092 @ 339,122: 19x25
#1093 @ 106,805: 24x12
#1094 @ 331,7: 28x18
#1095 @ 215,800: 18x29
#1096 @ 588,257: 19x20
#1097 @ 342,418: 21x21
#1098 @ 982,780: 11x18
#1099 @ 586,912: 26x25
#1100 @ 972,170: 12x10
#1101 @ 804,496: 21x18
#1102 @ 837,66: 12x17
#1103 @ 190,763: 17x19
#1104 @ 904,215: 20x27
#1105 @ 370,489: 29x22
#1106 @ 530,572: 20x18
#1107 @ 592,518: 12x28
#1108 @ 827,739: 24x10
#1109 @ 495,621: 13x20
#1110 @ 412,603: 10x28
#1111 @ 79,306: 17x17
#1112 @ 676,387: 19x25
#1113 @ 881,686: 13x17
#1114 @ 892,672: 14x14
#1115 @ 679,329: 12x17
#1116 @ 289,209: 19x19
#1117 @ 738,488: 26x12
#1118 @ 144,669: 25x12
#1119 @ 809,269: 10x17
#1120 @ 41,384: 23x12
#1121 @ 601,931: 24x19
#1122 @ 599,638: 25x15
#1123 @ 666,883: 25x10
#1124 @ 511,863: 28x29
#1125 @ 612,293: 20x13
#1126 @ 492,203: 25x17
#1127 @ 392,597: 19x15
#1128 @ 605,809: 27x16
#1129 @ 707,932: 12x25
#1130 @ 257,933: 15x20
#1131 @ 847,352: 18x23
#1132 @ 222,319: 27x23
#1133 @ 288,667: 13x25
#1134 @ 951,503: 14x17
#1135 @ 922,370: 22x12
#1136 @ 260,546: 28x19
#1137 @ 773,212: 19x26
#1138 @ 864,432: 11x12
#1139 @ 545,384: 27x18
#1140 @ 68,35: 11x26
#1141 @ 823,189: 25x23
#1142 @ 251,636: 29x23
#1143 @ 395,946: 12x22
#1144 @ 783,251: 11x14
#1145 @ 489,246: 12x24
#1146 @ 961,245: 13x19
#1147 @ 911,529: 29x25
#1148 @ 864,798: 21x14
#1149 @ 224,346: 13x25
#1150 @ 202,584: 28x21
#1151 @ 753,588: 10x16
#1152 @ 303,827: 27x19
#1153 @ 299,523: 12x12
#1154 @ 739,314: 12x20
#1155 @ 545,453: 11x12
#1156 @ 580,456: 15x11
#1157 @ 170,836: 18x15
#1158 @ 233,135: 20x20
#1159 @ 395,540: 21x21
#1160 @ 679,825: 13x17
#1161 @ 798,902: 20x12
#1162 @ 342,513: 20x19
#1163 @ 22,23: 24x29
#1164 @ 316,645: 29x18
#1165 @ 885,37: 25x24
#1166 @ 414,10: 14x17
#1167 @ 123,97: 23x18
#1168 @ 155,851: 27x29
#1169 @ 413,850: 25x12
#1170 @ 906,432: 24x15
#1171 @ 5,563: 25x27
#1172 @ 557,500: 10x25
#1173 @ 375,165: 23x25
#1174 @ 844,176: 20x17
#1175 @ 775,474: 26x16
#1176 @ 61,539: 17x14
#1177 @ 263,970: 22x14
#1178 @ 596,169: 12x12
#1179 @ 323,295: 29x25
#1180 @ 746,858: 14x21
#1181 @ 232,80: 24x14
#1182 @ 945,660: 15x14
#1183 @ 415,811: 27x25
#1184 @ 529,529: 13x23
#1185 @ 223,852: 27x28
#1186 @ 519,567: 10x12
#1187 @ 764,364: 13x11
#1188 @ 515,59: 25x17
#1189 @ 294,408: 24x28
#1190 @ 283,119: 29x15
#1191 @ 608,40: 19x21
#1192 @ 308,529: 14x10
#1193 @ 803,689: 25x24
#1194 @ 55,684: 11x21
#1195 @ 397,550: 18x20
#1196 @ 166,892: 17x28
#1197 @ 457,70: 28x22
#1198 @ 430,971: 20x16
#1199 @ 134,21: 29x20
#1200 @ 148,99: 15x23
#1201 @ 864,364: 26x12
#1202 @ 943,747: 17x14
#1203 @ 67,330: 3x5
#1204 @ 158,182: 27x18
#1205 @ 397,229: 29x16
#1206 @ 828,561: 28x25
#1207 @ 144,882: 21x14
#1208 @ 59,318: 22x23
#1209 @ 137,795: 23x29
#1210 @ 889,357: 17x27
#1211 @ 746,596: 24x17
#1212 @ 308,305: 24x27
#1213 @ 604,568: 23x19
#1214 @ 813,236: 29x13
#1215 @ 527,654: 9x9
#1216 @ 103,954: 12x10
#1217 @ 668,869: 11x25
#1218 @ 290,427: 10x22
#1219 @ 544,437: 16x23
#1220 @ 528,117: 21x16
#1221 @ 20,487: 23x16
#1222 @ 498,256: 12x27
#1223 @ 303,487: 14x25
#1224 @ 428,219: 17x23
#1225 @ 404,532: 21x24
#1226 @ 426,740: 22x26
#1227 @ 426,308: 25x13
#1228 @ 674,265: 24x19
#1229 @ 945,649: 19x23
#1230 @ 544,516: 14x20
#1231 @ 44,172: 22x13
#1232 @ 973,738: 15x14
#1233 @ 184,619: 11x17
#1234 @ 598,530: 15x22
#1235 @ 967,86: 10x11
#1236 @ 27,76: 26x19
#1237 @ 737,919: 26x19
#1238 @ 106,362: 11x12
#1239 @ 833,775: 27x23
#1240 @ 209,828: 24x12
#1241 @ 140,97: 13x15
#1242 @ 411,671: 11x16
#1243 @ 951,153: 21x18
#1244 @ 979,112: 14x29
#1245 @ 813,420: 21x15
#1246 @ 413,191: 25x16
#1247 @ 131,180: 29x16
#1248 @ 604,899: 29x15
#1249 @ 147,909: 17x10
#1250 @ 857,53: 29x14
#1251 @ 265,914: 11x17
#1252 @ 263,817: 18x27
#1253 @ 451,57: 27x23
#1254 @ 348,63: 27x11
#1255 @ 558,75: 12x23
#1256 @ 152,889: 25x19
#1257 @ 874,267: 11x13
#1258 @ 578,329: 28x14
#1259 @ 882,922: 16x16
#1260 @ 872,129: 20x18
#1261 @ 756,322: 21x12
#1262 @ 682,830: 27x14
#1263 @ 463,203: 14x19
#1264 @ 770,222: 28x17
#1265 @ 494,551: 11x27
#1266 @ 754,317: 29x29
#1267 @ 852,531: 25x17
#1268 @ 185,612: 19x20
#1269 @ 663,350: 19x11
#1270 @ 562,534: 19x19
#1271 @ 76,276: 26x20
#1272 @ 821,25: 23x13
#1273 @ 172,117: 23x20
#1274 @ 829,397: 13x19
#1275 @ 671,185: 16x16
#1276 @ 390,914: 14x19
#1277 @ 31,500: 25x27
#1278 @ 806,133: 24x13
#1279 @ 604,563: 26x22
#1280 @ 499,426: 18x25
#1281 @ 881,59: 21x11
#1282 @ 65,236: 25x16
#1283 @ 324,186: 13x20
#1284 @ 322,925: 28x22
#1285 @ 604,176: 10x10
#1286 @ 782,235: 17x22
#1287 @ 152,94: 10x27""".split('\n')

EXAMPLE_DATA = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".split('\n')

re_line = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
Instruction = namedtuple('inst', ['num', 'start', 'size'])
Location = namedtuple('loc', ['y', 'x'])

SIZE = 1000


def parse_line(line):
    match = re_line.match(line)
    assert match
    return Instruction(int(match.group(1)), Location(int(match.group(2)), int(match.group(3))),
                       Location(int(match.group(4)), int(match.group(5))))


def add_square(base, start, size):
    base[start.y:start.y+size.y, start.x:start.x+size.x] += 1


def overlaps(base, instruction):
    start = instruction.start
    size = instruction.size
    if base[start.y:start.y+size.y, start.x:start.x+size.x].sum() == size.x * size.y:
        print(instruction.num)


if __name__ == '__main__':
    world = np.zeros((SIZE, SIZE), dtype=np.int64)
    for inst in (parse_line(l) for l in DATA):
        add_square(world, inst.start, inst.size)
    print((world > 1).sum())
    for inst in (parse_line(l) for l in DATA):
        overlaps(world, inst)
