
### vn: K=4 b=2 a0=2 a-=1 K_f=3 (wall cap 4)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 3 | B2/S12 | chaos | 0.468 | 0.47703 | 1.4 | A=12: 220753/13615/3, 5.62, cv 1.00, ρ_f 0.46 ; A=20: 124852/13238/0, 7.09, cv 1.01, ρ_f 0.43 ; A=28: 37307/17892/0, 8.23, cv 0.99, ρ_f 0.42 | FACE LAW 0.163/cell strong |
| 4 | B23/S123 | chaos | 0.644 | 0.37836 | 1.93 | A=12: 0/7455/187468, ρ_f 1.00 ; A=20: 0/0/147731, ρ_f 1.00 ; A=28: 0/0/130998, ρ_f 1.00 | WALL |
| 5 | B234/S1234 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### cross2: K=8 b=3 a0=4 a-=2 K_f=6 (wall cap 7)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 4 | B3/S23 | die | None | - | - | A=12: 0/0/0, none survive burn-in ; A=20: 0/0/0, none survive burn-in | die |
| 5 | B34/S234 | chaos | 0.474 | 0.45579 | 1.12 | A=12: 124773/22942/984, 5.64, cv 1.01, ρ_f 0.59 ; A=20: 15841/2849/0, 9.13, cv 1.01, ρ_f 0.58 | FACE LAW 0.437/cell strong |
| 6 | B345/S2345 | freeze | 0.653 | 0.00806 | 2.13 | A=12: 2614/2797/63182, 7.81, cv 0.99, ρ_f 0.71 ; A=20: 7/13/151567, 16.21, ρ_f 0.70 | freeze |
| 7 | B3456/S23456 | freeze | 0.676 | 0.00867 | 2.29 | A=12: 0/138/14589, ρ_f 1.00 ; A=20: 0/0/15959, ρ_f 1.00 | freeze |
| 8 | B34567/S234567 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in ; A=20: 0/0/0, none survive burn-in | freeze |
| 9 | B345678/S2345678 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in ; A=20: 0/0/0, none survive burn-in | freeze |

### cross3: K=12 b=4 a0=6 a-=3 K_f=9 (wall cap 10)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 5 | B4/S34 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 6 | B45/S345 | chaos | 0.392 | 0.46336 | 0.42 | A=12: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 7 | B456/S3456 | chaos | 0.452 | 0.48539 | 0.65 | A=12: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 8 | B4567/S34567 | chaos | 0.502 | 0.48742 | 0.88 | A=12: 3/0/0, 3.15, ρ_f 0.88 | unclear |
| 9 | B45678/S345678 | chaos | 0.554 | 0.47254 | 1.19 | A=12: 54/32/1, 4.32, cv 0.98, ρ_f 0.79 ; A=20: 25951/37915/121, 7.82, cv 1.00, ρ_f 0.76 ; A=28: 1167/12783/0, 10.97, cv 1.01, ρ_f 0.76 | FACE LAW 0.416/cell strong |
| 10 | B456789/S3456789 | chaos | 0.615 | 0.42984 | 1.63 | A=12: 0/4965/802, ρ_f 1.00 ; A=20: 0/47962/733, ρ_f 1.00 ; A=28: 0/1799/4, ρ_f 1.00 | WALL |
| 11 | B456789(10)/S3456789(10) | chaos | 0.69 | 0.32409 | 2.3 | A=12: 0/9393/11551, ρ_f 1.00 ; A=20: 0/19751/35420, ρ_f 1.00 ; A=28: 0/1136/6581, ρ_f 1.00 | WALL |
| 12 | cap 12 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 13 | cap 13 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### cross4: K=16 b=5 a0=8 a-=4 K_f=12 (wall cap 13)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 6 | B5/S45 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 7 | B56/S456 | chaos | 0.334 | 0.42375 | 0.11 | A=12: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 8 | B567/S4567 | chaos | 0.401 | 0.47819 | 0.23 | A=12: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 9 | B5678/S45678 | chaos | 0.436 | 0.48955 | 0.32 | A=12: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 10 | B56789/S456789 | chaos | 0.478 | 0.49428 | 0.47 | A=12: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 11 | B56789(10)/S456789(10) | chaos | 0.524 | 0.47881 | 0.68 | A=12: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 12 | cap 12 | chaos | 0.566 | 0.46837 | 0.93 | A=12: 20/4/3, 4.19, cv 1.11, ρ_f 0.88 ; A=20: 25814/27871/3218, 6.61, cv 1.00, ρ_f 0.79 ; A=28: 7233/19057/240, 8.76, cv 0.98, ρ_f 0.79 | FACE LAW 0.286/cell strong |
| 13 | cap 13 | chaos | 0.608 | 0.44098 | 1.23 | A=12: 0/4487/6866, ρ_f 1.00 ; A=20: 0/55683/14788, ρ_f 1.00 ; A=28: 0/11912/1945, ρ_f 1.00 | WALL |
| 14 | cap 14 | chaos | 0.657 | 0.38923 | 1.68 | A=12: 0/18/327, ρ_f 1.00 ; A=20: 0/35616/42470, ρ_f 1.00 ; A=28: 0/5497/5131, ρ_f 1.00 | WALL |
| 15 | cap 15 | freeze | 0.751 | 0.01318 | 2.86 | A=12: 0/0/0, none survive burn-in | freeze |
| 16 | cap 16 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 17 | cap 17 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### moore: K=8 b=4 a0=2 a-=3 K_f=5 (wall cap 6)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 5 | B4/S34 | die | None | - | - | A=12: 0/0/0, none survive burn-in ; A=20: 0/0/0, none survive burn-in | die |
| 6 | B45/S345 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in ; A=20: 0/0/0, none survive burn-in | freeze |
| 7 | B456/S3456 | chaos | 0.593 | 0.42393 | 0.63 | A=12: 28316/5897/4, 4.91, cv 1.00, ρ_f 0.59 ; A=20: 20515/32496/0, 6.16, cv 1.00, ρ_f 0.54 | FACE LAW 0.156/cell strong |
| 8 | B4567/S34567 | glass | 0.789 | 0.02924 | 1.47 | A=12: 0/0/35761, ρ_f 1.00 ; A=20: 0/0/34107, ρ_f 1.00 | WALL |
| 9 | B45678/S345678 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in ; A=20: 0/0/0, none survive burn-in | freeze |

### moore_r2: K=24 b=11 a0=4 a-=10 K_f=14 (wall cap 15)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 12 | B(11)/S(10)(11) | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 13 | B(11)(12)/S(10)(11)(12) | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 14 | cap 14 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 15 | cap 15 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 16 | cap 16 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 17 | cap 17 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 18 | cap 18 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 19 | cap 19 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 20 | cap 20 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 21 | cap 21 | glass | 0.594 | 0.41645 | 0.03 | A=12: 0/0/0, none survive burn-in ; A=20: 0/0/0, none survive burn-in ; A=28: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 22 | cap 22 | chaos | 0.579 | 0.34359 | 0.02 | A=12: 0/286/433, ρ_f 1.00 ; A=20: 0/8165/12643, ρ_f 1.00 ; A=28: 0/442/421, ρ_f 1.00 | WALL |
| 23 | cap 23 | freeze | 0.114 | 0.02405 | 0.0 | A=12: 0/0/0, none survive burn-in | freeze |
| 24 | cap 24 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 25 | cap 25 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### star2: K=12 b=5 a0=4 a-=4 K_f=8 (wall cap 9)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 6 | B5/S45 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 7 | B56/S456 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 8 | B567/S4567 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 9 | B5678/S45678 | chaos | 0.527 | 0.49646 | 0.39 | A=12: 0/18609/120, ρ_f 1.00 ; A=20: 0/22519/0, ρ_f 1.00 ; A=28: 0/634/0, ρ_f 1.00 | WALL |
| 10 | B56789/S456789 | chaos | 0.59 | 0.47367 | 0.61 | A=12: 0/27922/141, ρ_f 1.00 ; A=20: 0/17046/0, ρ_f 1.00 ; A=28: 0/391/0, ρ_f 1.00 | WALL |
| 11 | B56789(10)/S456789(10) | chaos | 0.639 | 0.42512 | 0.83 | A=12: 0/28040/192, ρ_f 1.00 ; A=20: 0/16128/0, ρ_f 1.00 ; A=28: 0/279/0, ρ_f 1.00 | WALL |
| 12 | cap 12 | freeze | 0.832 | 0.01705 | 2.39 | A=12: 0/6/580, ρ_f 1.00 | freeze |
| 13 | cap 13 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### tri6: K=6 b=3 a0=2 a-=2 K_f=4 (wall cap 5)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 4 | B3/S23 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 5 | B34/S234 | freeze | 0.664 | 0.01042 | 1.32 | A=12: 0/21880/54054, ρ_f 1.00 | freeze |
| 6 | B345/S2345 | freeze | 0.755 | 0.0236 | 1.71 | A=12: 0/0/107, ρ_f 1.00 | freeze |
| 7 | B3456/S23456 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### tri12: K=12 b=6 a0=2 a-=5 K_f=7 (wall cap 8)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 7 | B6/S56 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 8 | B67/S567 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 9 | B678/S5678 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 10 | B6789/S56789 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 11 | B6789(10)/S56789(10) | chaos | 0.606 | 0.37057 | 0.25 | A=12: 0/13971/10109, ρ_f 1.00 ; A=20: 0/35/9, ρ_f 1.00 ; A=28: 0/0/0, ρ_f 1.00 | WALL |
| 12 | cap 12 | freeze | 0.82 | 0.00793 | 1.11 | A=12: 0/0/154, ρ_f 1.00 | freeze |
| 13 | cap 13 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### tri18: K=18 b=8 a0=4 a-=7 K_f=11 (wall cap 12)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 9 | B8/S78 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 10 | B89/S789 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 11 | B89(10)/S789(10) | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 12 | B89(10)(11)/S789(10)(11) | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 13 | cap 13 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 14 | cap 14 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 15 | cap 15 | chaos | 0.577 | 0.45048 | 0.11 | A=12: 0/0/0, none survive burn-in ; A=20: 253/32/0, 4.25, cv 0.96, ρ_f 0.54 ; A=28: 543/256/0, 4.94, cv 1.06, ρ_f 0.49 | faces die, gain +0.70 (+0.087/cell) |
| 16 | cap 16 | chaos | 0.623 | 0.42998 | 0.18 | A=12: 0/405/47, ρ_f 1.00 ; A=20: 0/36136/197, ρ_f 1.00 ; A=28: 0/2190/2, ρ_f 1.00 | WALL |
| 17 | cap 17 | chaos | 0.669 | 0.38208 | 0.3 | A=12: 0/525/130, ρ_f 1.00 ; A=20: 0/35031/293, ρ_f 1.00 ; A=28: 0/2075/2, ρ_f 1.00 | WALL |
| 18 | cap 18 | freeze | 0.466 | 0.01556 | 0.02 | A=12: 0/0/21, ρ_f 1.00 | freeze |
| 19 | cap 19 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### tristar2: K=12 b=5 a0=4 a-=4 K_f=8 (wall cap 9)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 6 | B5/S45 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 7 | B56/S456 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 8 | B567/S4567 | chaos | 0.643 | 0.05888 | 0.85 | A=12: 15/1/24, 5.34, cv 1.51, ρ_f 0.66 ; A=20: 258/907/8625, 11.31, cv 1.08, ρ_f 0.67 ; A=28: 31/133/6993, 11.33, cv 3.82, ρ_f 0.69 | chaos, settles (+0.002) |
| 9 | B5678/S45678 | freeze | 0.664 | 0.00669 | 0.97 | A=12: 0/5086/6064, ρ_f 1.00 | freeze |
| 10 | B56789/S456789 | freeze | 0.681 | 0.01685 | 1.07 | A=12: 0/168/1710, ρ_f 1.00 | freeze |
| 11 | B56789(10)/S456789(10) | freeze | 0.694 | 0.01325 | 1.16 | A=12: 0/239/3420, ρ_f 1.00 | freeze |
| 12 | cap 12 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 13 | cap 13 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### tristar3: K=18 b=7 a0=6 a-=6 K_f=12 (wall cap 13)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 8 | B7/S67 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 9 | B78/S678 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 10 | B789/S6789 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 11 | B789(10)/S6789(10) | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 12 | cap 12 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 13 | cap 13 | chaos | 0.502 | 0.48956 | 0.11 | A=12: 0/0/0, none survive burn-in ; A=20: 0/38123/367, ρ_f 1.00 ; A=28: 0/5834/5, ρ_f 1.00 | WALL |
| 14 | cap 14 | chaos | 0.546 | 0.48519 | 0.19 | A=12: 0/1/0, none survive burn-in ; A=20: 0/38885/464, ρ_f 1.00 ; A=28: 0/5704/4, ρ_f 1.00 | WALL |
| 15 | cap 15 | chaos | 0.586 | 0.47651 | 0.28 | A=12: 0/0/0, none survive burn-in ; A=20: 0/31592/2468, ρ_f 1.00 ; A=28: 0/7334/107, ρ_f 1.00 | WALL |
| 16 | cap 16 | chaos | 0.639 | 0.44244 | 0.47 | A=12: 0/0/0, none survive burn-in ; A=20: 0/36113/5811, ρ_f 1.00 ; A=28: 0/6557/156, ρ_f 1.00 | WALL |
| 17 | cap 17 | chaos | 0.687 | 0.37713 | 0.73 | A=12: 0/0/0, none survive burn-in ; A=20: 0/13528/24934, ρ_f 1.00 ; A=28: 0/7515/8908, ρ_f 1.00 | WALL |
| 18 | cap 18 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 19 | cap 19 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### hex3: K=3 b=2 a0=1 a-=1 K_f=2 (wall cap 3)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 3 | B2/S12 | glass | 0.536 | 0.01908 | 1.07 | A=24: 0/0/0, none survive burn-in ; A=40: 0/0/0, none survive burn-in ; A=56: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 4 | B23/S123 | freeze | None | - | - | A=24: 0/0/0, none survive burn-in | freeze |

### hex9: K=9 b=5 a0=2 a-=4 K_f=6 (wall cap 7)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 6 | B5/S45 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 7 | B56/S456 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 8 | B567/S4567 | glass | 0.199 | 0.00546 | 0.0 | A=12: 0/0/0, none survive burn-in ; A=20: 0/0/0, none survive burn-in ; A=28: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 9 | B5678/S45678 | glass | 0.669 | 0.01727 | 0.6 | A=12: 0/0/12, ρ_f 0.99 ; A=20: 0/0/2, ρ_f 1.00 ; A=28: 0/0/0, none survive burn-in | WALL |
| 10 | B56789/S456789 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### hex12: K=12 b=6 a0=2 a-=5 K_f=7 (wall cap 8)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 7 | B6/S56 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 8 | B67/S567 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 9 | B678/S5678 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 10 | B6789/S56789 | die | None | - | - | A=12: 0/0/0, none survive burn-in | die |
| 11 | B6789(10)/S56789(10) | chaos | 0.623 | 0.39353 | 0.28 | A=12: 3098/37/42, 4.25, cv 1.06, ρ_f 0.71 ; A=20: 32170/303/5, 5.05, cv 1.01, ρ_f 0.68 ; A=28: 41632/1111/6, 5.65, cv 1.01, ρ_f 0.66 | FACE LAW 0.087/cell weak |
| 12 | cap 12 | glass | 0.828 | 0.03084 | 1.17 | A=12: 0/0/5792, ρ_f 0.95 ; A=20: 0/0/13493, ρ_f 0.95 ; A=28: 0/0/11792, ρ_f 0.96 | unclear |
| 13 | cap 13 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### kagome4: K=4 b=3 a0=0 a-=2 K_f=3 (wall cap 4)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 4 | B3/S23 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 5 | B34/S234 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### kagome6: K=6 b=3 a0=2 a-=2 K_f=4 (wall cap 5)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 4 | B3/S23 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |
| 5 | B34/S234 | glass | 0.661 | 0.00965 | 1.31 | A=12: 0/0/211785, ρ_f 1.00 ; A=20: 0/0/148273, ρ_f 1.00 ; A=28: 0/0/104670, ρ_f 1.00 | WALL |
| 6 | B345/S2345 | chaos | 0.697 | 0.24979 | 1.46 | A=12: 0/2/179446, ρ_f 1.00 ; A=20: 0/0/130183, ρ_f 1.00 ; A=28: 0/0/101809, ρ_f 1.00 | WALL |
| 7 | B3456/S23456 | freeze | None | - | - | A=12: 0/0/0, none survive burn-in | freeze |

### kagome8: K=8 b=5 a0=0 a-=4 K_f=5 (wall cap 6)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 6 | B5/S45 | die | None | - | - | A=24: 0/0/0, none survive burn-in | die |
| 7 | B56/S456 | die | None | - | - | A=24: 0/0/0, none survive burn-in | die |
| 8 | B567/S4567 | freeze | 0.476 | 0.00321 | 0.05 | A=24: 0/0/0, none survive burn-in | freeze |
| 9 | B5678/S45678 | freeze | None | - | - | A=24: 0/0/0, none survive burn-in | freeze |

### gump: K=12 b=4 a0=6 a-=3 K_f=9 (wall cap 10)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 5 | B4/S34 | die | None | - | - | A=27: 0/0/0, none survive burn-in ; A=48: 0/0/0, none survive burn-in | die |
| 6 | B45/S345 | chaos | 0.419 | 0.45513 | 0.51 | A=27: 119619/1362/45, 5.48, cv 1.00, ρ_f 0.50 ; A=48: 5021/10/0, 9.91, cv 1.03, ρ_f 0.52 | FACE LAW 0.211/cell strong |
| 7 | B456/S3456 | chaos | 0.482 | 0.43269 | 0.78 | A=27: 117790/3466/186, 5.42, cv 1.01, ρ_f 0.59 ; A=48: 5870/57/2, 9.88, cv 0.98, ρ_f 0.61 | FACE LAW 0.213/cell strong |
| 8 | B4567/S34567 | chaos | 0.548 | 0.36811 | 1.15 | A=27: 164161/7102/14629, 5.98, cv 1.00, ρ_f 0.70 ; A=48: 4374/88/4, 10.34, cv 1.00, ρ_f 0.71 | FACE LAW 0.208/cell strong |
| 9 | B45678/S345678 | glass | 0.615 | 0.06068 | 1.63 | A=27: 45890/8033/165883, 7.70, cv 1.00, ρ_f 0.81 ; A=48: 2/1/306, 12.48, ρ_f 0.81 | unclear |
| 10 | B456789/S3456789 | freeze | 0.666 | 0.02371 | 2.07 | A=27: 0/7935/217388, ρ_f 1.00 ; A=48: 0/6/134334, ρ_f 1.00 | freeze |
| 11 | B456789(10)/S3456789(10) | freeze | 0.716 | 0.02233 | 2.57 | A=27: 0/0/769, ρ_f 1.00 ; A=48: 0/0/8345, ρ_f 1.00 | freeze |
| 12 | cap 12 | freeze | None | - | - | A=27: 0/0/0, none survive burn-in ; A=48: 0/0/0, none survive burn-in | freeze |

### bond10: K=10 b=4 a0=4 a-=3 K_f=7 (wall cap 8)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 5 | B4/S34 | freeze | None | - | - | A=27: 0/0/0, none survive burn-in | freeze |
| 6 | B45/S345 | chaos | 0.438 | 0.48349 | 0.42 | A=27: 5638/735/488, 4.51, cv 1.01, ρ_f 0.41 ; A=48: 40357/11486/4166, 6.06, cv 1.00, ρ_f 0.39 ; A=75: 14044/14588/2052, 7.49, cv 1.00, ρ_f 0.38 | FACE LAW 0.062/cell weak |
| 7 | B456/S3456 | chaos | 0.527 | 0.48309 | 0.73 | A=27: 45712/9917/687, 8.25, cv 1.00, ρ_f 0.73 ; A=48: 25/1/0, 13.47, cv 0.71, ρ_f 0.74 ; A=75: 0/0/0, ρ_f 0.74 | faces die, gain +5.22 (+0.249/cell) |
| 8 | B4567/S34567 | chaos | 0.602 | 0.42446 | 1.09 | A=27: 0/98649/7892, ρ_f 1.00 ; A=48: 0/100/5, ρ_f 1.00 ; A=75: 0/0/0, ρ_f 1.00 | WALL |
| 9 | B45678/S345678 | chaos | 0.668 | 0.3032 | 1.49 | A=27: 0/8842/113188, ρ_f 1.00 ; A=48: 0/12/113495, ρ_f 1.00 ; A=75: 0/0/72728, ρ_f 1.00 | WALL |

### face8: K=8 b=3 a0=4 a-=2 K_f=6 (wall cap 7)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 4 | B3/S23 | die | None | - | - | A=27: 0/0/0, none survive burn-in | die |
| 5 | B34/S234 | chaos | 0.48 | 0.44808 | 1.15 | A=27: 10265/561/22, 9.97, cv 1.02, ρ_f 0.60 ; A=48: 3/0/0, 13.90, ρ_f 0.60 | unclear |
| 6 | B345/S2345 | freeze | 0.654 | 0.01007 | 2.14 | A=27: 230/97/86732, 11.36, cv 0.95, ρ_f 0.73 | freeze |
| 7 | B3456/S23456 | freeze | 0.683 | 0.01183 | 2.34 | A=27: 0/210/71892, ρ_f 1.00 | freeze |
| 8 | B34567/S234567 | freeze | None | - | - | A=27: 0/0/0, none survive burn-in | freeze |

### face18: K=18 b=6 a0=8 a-=5 K_f=13 (wall cap 14)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 7 | B6/S56 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 8 | B67/S567 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 9 | B678/S5678 | chaos | 0.401 | 0.49122 | 0.09 | A=25: 3343/113/5, 4.35, cv 0.99, ρ_f 0.45 ; A=49: 17437/2288/3, 7.33, cv 0.99, ρ_f 0.47 ; A=81: 475/261/0, 10.70, cv 0.95, ρ_f 0.47 | FACE LAW 0.113/cell |
| 10 | B6789/S56789 | chaos | 0.448 | 0.51596 | 0.16 | A=25: 29357/2663/145, 5.28, cv 1.01, ρ_f 0.55 ; A=49: 1226/1087/0, 10.38, cv 1.00, ρ_f 0.57 ; A=81: 1/28/0, 15.45, ρ_f 0.57 | FACE LAW 0.212/cell strong |
| 11 | B6789(10)/S56789(10) | chaos | 0.486 | 0.51581 | 0.24 | A=25: 39271/4917/380, 5.59, cv 1.01, ρ_f 0.62 ; A=49: 612/962/0, 11.17, cv 1.05, ρ_f 0.64 ; A=81: 0/16/0, ρ_f 0.65 | FACE LAW 0.232/cell strong |
| 12 | cap 12 | chaos | 0.529 | 0.51064 | 0.37 | A=25: 47485/6282/1075, 5.87, cv 1.00, ρ_f 0.70 ; A=49: 496/605/2, 11.41, cv 1.00, ρ_f 0.72 ; A=81: 0/6/0, ρ_f 0.73 | FACE LAW 0.231/cell strong |
| 13 | cap 13 | chaos | 0.558 | 0.49524 | 0.49 | A=25: 50254/7916/2471, 6.31, cv 1.00, ρ_f 0.81 ; A=49: 154/94/1, 12.33, cv 0.95, ρ_f 0.84 ; A=81: 0/2/0, ρ_f 0.84 | FACE LAW 0.250/cell strong |
| 14 | cap 14 | chaos | 0.597 | 0.46627 | 0.68 | A=25: 0/28810/38036, ρ_f 1.00 ; A=49: 0/23/9, ρ_f 1.00 ; A=81: 0/0/0, ρ_f 1.00 | WALL |
| 15 | cap 15 | chaos | 0.637 | 0.42956 | 0.94 | A=25: 0/21713/40160, ρ_f 1.00 ; A=49: 0/5/3, ρ_f 1.00 ; A=81: 0/0/0, ρ_f 1.00 | WALL |

### fcc: K=12 b=4 a0=6 a-=3 K_f=9 (wall cap 10)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 5 | B4/S34 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 6 | B45/S345 | chaos | 0.394 | 0.48194 | 0.43 | A=25: 9445/1523/10, 4.61, cv 1.01, ρ_f 0.45 ; A=49: 6189/101/0, 9.24, cv 1.01, ρ_f 0.46 ; A=81: 17/0/0, 12.60, cv 0.61, ρ_f 0.46 | FACE LAW 0.193/cell strong |
| 7 | B456/S3456 | chaos | 0.46 | 0.51198 | 0.68 | A=25: 357/143/2, 4.08, cv 1.00, ρ_f 0.54 ; A=49: 6466/373/0, 9.34, cv 1.00, ρ_f 0.57 ; A=81: 11/0/0, 12.84, cv 0.48, ρ_f 0.57 | FACE LAW 0.219/cell strong |
| 8 | B4567/S34567 | chaos | 0.514 | 0.51703 | 0.95 | A=25: 67/26/0, 4.03, cv 1.05, ρ_f 0.62 ; A=49: 8081/931/0, 9.24, cv 1.01, ρ_f 0.66 ; A=81: 22/1/0, 12.90, cv 0.62, ρ_f 0.67 | faces die, gain +8.87 (+0.158/cell) |
| 9 | B45678/S345678 | chaos | 0.568 | 0.48906 | 1.28 | A=25: 1460/1674/51, 4.93, cv 1.01, ρ_f 0.75 ; A=49: 1391/1336/0, 11.08, cv 1.02, ρ_f 0.78 ; A=81: 1/2/0, 14.17, ρ_f 0.78 | FACE LAW 0.256/cell strong |
| 10 | B456789/S3456789 | chaos | 0.625 | 0.44691 | 1.71 | A=25: 0/10974/3837, ρ_f 1.00 ; A=49: 0/3494/179, ρ_f 1.00 ; A=81: 0/1/1, ρ_f 1.00 | WALL |
| 11 | B456789(10)/S3456789(10) | chaos | 0.68 | 0.34709 | 2.2 | A=25: 0/31162/15090, ρ_f 1.00 ; A=49: 0/1609/214, ρ_f 1.00 ; A=81: 0/2/0, ρ_f 1.00 | WALL |

### bcc8: K=8 b=3 a0=4 a-=2 K_f=6 (wall cap 7)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 4 | B3/S23 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 5 | B34/S234 | chaos | 0.466 | 0.49869 | 1.09 | A=25: 55972/2532/0, 8.27, cv 1.00, ρ_f 0.58 ; A=49: 7/0/0, 13.96, ρ_f 0.59 ; A=81: 0/0/0, ρ_f 0.59 | unclear |
| 6 | B345/S2345 | chaos | 0.543 | 0.478 | 1.47 | A=25: 29860/14257/10, 9.10, cv 1.00, ρ_f 0.72 ; A=49: 1/0/0, 13.78, ρ_f 0.73 | unclear |
| 7 | B3456/S23456 | chaos | 0.645 | 0.38709 | 2.08 | A=25: 0/5302/248186, ρ_f 1.00 ; A=49: 0/0/148642, ρ_f 1.00 ; A=81: 0/0/108296, ρ_f 1.00 | WALL |
| 8 | B34567/S234567 | freeze | None | - | - | A=25: 0/6/399, ρ_f 1.00 | freeze |

### bcc14: K=14 b=5 a0=6 a-=4 K_f=10 (wall cap 11)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 6 | B5/S45 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 7 | B56/S456 | chaos | 0.371 | 0.45206 | 0.13 | A=25: 0/0/0, none survive burn-in ; A=49: 3/0/0, 2.73, ρ_f 0.32 ; A=81: 6/0/0, 3.39, ρ_f 0.19 | unclear |
| 8 | B567/S4567 | chaos | 0.444 | 0.51858 | 0.27 | A=25: 117/34/0, 4.11, cv 0.93, ρ_f 0.52 ; A=49: 15271/567/1, 8.32, cv 1.02, ρ_f 0.56 ; A=81: 47/0/0, 12.39, cv 0.65, ρ_f 0.56 | faces die, gain +8.28 (+0.148/cell) |
| 9 | B5678/S45678 | chaos | 0.499 | 0.52461 | 0.43 | A=25: 57/31/1, 4.12, cv 0.93, ρ_f 0.63 ; A=49: 11109/996/0, 8.68, cv 1.01, ρ_f 0.67 ; A=81: 23/2/0, 12.80, cv 0.56, ρ_f 0.67 | faces die, gain +8.68 (+0.155/cell) |
| 10 | B56789/S456789 | chaos | 0.539 | 0.512 | 0.59 | A=25: 155/163/1, 4.51, cv 0.99, ρ_f 0.74 ; A=49: 5532/1913/5, 9.51, cv 1.03, ρ_f 0.79 ; A=81: 2/3/0, 13.19, ρ_f 0.80 | FACE LAW 0.208/cell strong |
| 11 | B56789(10)/S456789(10) | chaos | 0.593 | 0.4767 | 0.87 | A=25: 0/253/107, ρ_f 1.00 ; A=49: 0/5904/298, ρ_f 1.00 ; A=81: 0/7/0, ρ_f 1.00 | WALL |
| 12 | cap 12 | chaos | 0.651 | 0.43383 | 1.26 | A=25: 0/1899/755, ρ_f 1.00 ; A=49: 0/5079/199, ρ_f 1.00 ; A=81: 0/2/0, ρ_f 1.00 | WALL |

### sc6: K=6 b=2 a0=4 a-=1 K_f=5 (wall cap 6)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 3 | B2/S12 | chaos | 0.374 | 0.42714 | 1.87 | A=25: 33422/158/0, 9.20, cv 1.00, ρ_f 0.42 ; A=49: 3/0/0, 13.69, ρ_f 0.42 | unclear |
| 4 | B23/S123 | chaos | 0.495 | 0.40814 | 2.47 | A=25: 63117/1631/0, 8.66, cv 1.00, ρ_f 0.57 ; A=49: 7/0/0, 14.20, ρ_f 0.57 ; A=81: 0/0/0, ρ_f 0.57 | unclear |
| 5 | B234/S1234 | chaos | 0.613 | 0.30661 | 3.06 | A=25: 13625/3514/3188, 10.21, cv 1.00, ρ_f 0.71 ; A=49: 1/0/23, 17.28, ρ_f 0.72 ; A=81: 0/0/1022, ρ_f 0.72 | unclear |
| 6 | B2345/S12345 | freeze | None | - | - | A=25: 0/0/0, none survive burn-in | freeze |
| 7 | B23456/S123456 | freeze | None | - | - | A=25: 0/0/0, none survive burn-in | freeze |

### sc18: K=18 b=6 a0=8 a-=5 K_f=13 (wall cap 14)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 7 | B6/S56 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 8 | B67/S567 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 9 | B678/S5678 | chaos | 0.391 | 0.4919 | 0.08 | A=25: 0/0/0, none survive burn-in ; A=49: 9548/383/4, 4.73, cv 1.01, ρ_f 0.42 ; A=81: 20608/324/0, 7.06, cv 1.00, ρ_f 0.43 | FACE LAW 0.073/cell weak |
| 10 | B6789/S56789 | chaos | 0.439 | 0.53131 | 0.15 | A=25: 0/0/0, none survive burn-in ; A=49: 36841/7116/18, 5.87, cv 1.00, ρ_f 0.53 ; A=81: 1781/126/0, 10.00, cv 1.01, ρ_f 0.55 | FACE LAW 0.129/cell |
| 11 | B6789(10)/S56789(10) | chaos | 0.478 | 0.53336 | 0.23 | A=25: 0/0/0, none survive burn-in ; A=49: 34027/8685/43, 5.76, cv 1.01, ρ_f 0.60 ; A=81: 2188/141/0, 9.85, cv 0.96, ρ_f 0.62 | FACE LAW 0.128/cell |
| 12 | cap 12 | chaos | 0.522 | 0.51578 | 0.35 | A=25: 0/0/0, none survive burn-in ; A=49: 32458/11645/54, 5.88, cv 1.00, ρ_f 0.67 ; A=81: 2034/197/0, 9.96, cv 1.04, ρ_f 0.70 | FACE LAW 0.128/cell |
| 13 | cap 13 | chaos | 0.548 | 0.49997 | 0.44 | A=25: 0/0/0, none survive burn-in ; A=49: 30655/21886/124, 6.46, cv 1.00, ρ_f 0.79 ; A=81: 458/239/0, 11.44, cv 1.06, ρ_f 0.82 | FACE LAW 0.156/cell strong |
| 14 | cap 14 | chaos | 0.605 | 0.47391 | 0.73 | A=25: 0/0/0, none survive burn-in ; A=49: 0/55763/7072, ρ_f 1.00 ; A=81: 0/749/26, ρ_f 1.00 | WALL |
| 15 | cap 15 | chaos | 0.645 | 0.4468 | 1.0 | A=25: 0/0/0, none survive burn-in ; A=49: 0/54418/7972, ρ_f 1.00 ; A=81: 0/675/29, ρ_f 1.00 | WALL |

### sc26: K=26 b=10 a0=8 a-=9 K_f=17 (wall cap 18)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 11 | B(10)/S9(10) | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 12 | B(10)(11)/S9(10)(11) | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 13 | cap 13 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 14 | cap 14 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 15 | cap 15 | die | None | - | - | A=25: 0/0/0, none survive burn-in | die |
| 16 | cap 16 | glass | 0.455 | 0.47986 | 0.01 | A=25: 0/0/0, none survive burn-in ; A=49: 0/0/0, none survive burn-in ; A=81: 0/0/0, none survive burn-in | faces die before burn-in at these sizes |
| 17 | cap 17 | chaos | 0.513 | 0.5179 | 0.02 | A=25: 0/0/0, none survive burn-in ; A=49: 43/7/0, 3.90, cv 1.38, ρ_f 0.61 ; A=81: 5184/4509/0, 6.34, cv 1.01, ρ_f 0.63 | faces die, gain +2.44 (+0.076/cell) |
| 18 | cap 18 | chaos | 0.535 | 0.50135 | 0.03 | A=25: 0/0/0, none survive burn-in ; A=49: 1879/937/0, 4.97, cv 1.04, ρ_f 0.74 ; A=81: 1464/8848/0, 9.18, cv 0.95, ρ_f 0.81 | FACE LAW 0.132/cell |
| 19 | cap 19 | chaos | 0.548 | 0.4828 | 0.04 | A=25: 0/0/0, none survive burn-in ; A=49: 4621/3960/2, 5.67, cv 1.01, ρ_f 0.79 ; A=81: 374/6380/1, 10.78, cv 1.11, ρ_f 0.85 | FACE LAW 0.160/cell strong |

### cross3d2: K=12 b=3 a0=8 a-=2 K_f=10 (wall cap 11)

| c | rule | torus | ρ | act | R₁ | face sizes: deaths / sealed / settled, ln τ, CV, face density | verdict |
|---|---|---|---|---|---|---|---|
| 4 | B3/S23 | chaos | 0.286 | 0.38312 | 0.74 | A=25: 3441/17/0, 4.16, cv 0.99, ρ_f 0.30 ; A=49: 16780/0/0, 8.28, cv 1.00, ρ_f 0.32 ; A=81: 34/0/0, 12.63, cv 0.64, ρ_f 0.32 | faces die, gain +8.47 (+0.151/cell) |
| 5 | B34/S234 | chaos | 0.377 | 0.39684 | 1.28 | A=25: 104/1/0, 3.61, cv 1.02, ρ_f 0.40 ; A=49: 24587/19/0, 7.73, cv 0.99, ρ_f 0.41 ; A=81: 92/0/0, 12.17, cv 0.83, ρ_f 0.42 | FACE LAW 0.153/cell strong |
| 6 | B345/S2345 | chaos | 0.443 | 0.38023 | 1.77 | A=25: 0/0/0, none survive burn-in ; A=49: 36711/61/0, 7.40, cv 1.00, ρ_f 0.49 ; A=81: 255/0/0, 11.86, cv 1.00, ρ_f 0.49 | FACE LAW 0.139/cell |
| 7 | B3456/S23456 | chaos | 0.476 | 0.36381 | 2.04 | A=25: 0/0/0, none survive burn-in ; A=49: 44917/374/5, 7.22, cv 1.00, ρ_f 0.55 ; A=81: 92/0/79, 12.21, cv 1.23, ρ_f 0.65 | FACE LAW 0.156/cell strong |
| 8 | B34567/S234567 | chaos | 0.541 | 0.35766 | 2.63 | A=25: 0/0/0, none survive burn-in ; A=49: 43141/876/84, 7.37, cv 1.01, ρ_f 0.62 ; A=81: 321/0/3675, 12.07, cv 1.00, ρ_f 0.63 | FACE LAW 0.147/cell |
| 9 | B345678/S2345678 | chaos | 0.575 | 0.32916 | 2.97 | A=25: 0/0/0, none survive burn-in ; A=49: 17952/927/1839, 8.49, cv 0.99, ρ_f 0.70 ; A=81: 40/0/2785, 14.18, cv 1.03, ρ_f 0.71 | FACE LAW 0.178/cell strong |
| 10 | B3456789/S23456789 | chaos | 0.657 | 0.26108 | 3.89 | A=25: 219/24/125, 4.00, cv 1.03, ρ_f 0.73 ; A=49: 422/163/39173, 12.19, cv 1.02, ρ_f 0.80 ; A=81: 1/0/7967, 17.87, ρ_f 0.80 | chaos, settles (+0.341) |
| 11 | cap 11 | freeze | None | - | - | A=25: 0/0/2, ρ_f 1.00 | freeze |
| 12 | cap 12 | freeze | None | - | - | A=25: 0/0/0, none survive burn-in | freeze |
