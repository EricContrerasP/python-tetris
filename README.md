# python-tetris

Tetris game in pygame

  

## How to install

Para poder jugar tetris en python debes instalar la libreria [pygame](https://www.pygame.org/news) con el siguiente comando:

```

$ pip install pygame

```

## How to play

### How to init game

corre el comando en el mismo ambiente que instaló pygame:
```
$ python tetris.py
```

## Controls

- **⬅️ y ➡️: movimiento horizontal**
- **⬆️: rotación de 90° en sentido horario**
-   **⬇️: soft drop**
-   **Barra espaciadora: hard drop**
-   **Tecla Z o Left-Control: rotación de 90° en sentido antihorario**
-   **Tecla C o Shift: Retener pieza**
-   **Tecla R: reinicia el juego**

Al completar una fila, se eliminan todas las piezas de la misma, luego caen las piezas que se encuentran por sobre la fila eliminada.

Se observa la sombra de la pieza, de modo que se pre-visualiza como quedaria la pieza luego de un hard drop.

En cualquier momento, desde que un tetrominó entra en el campo de juego hasta que se bloquea, el jugador puede pulsar el botón Retener para mover el tetrominó activo al espacio de retención y mover el tetrominó que estaba en el espacio de retención a la parte superior del campo de juego. Un tetrominó movido al espacio de retención no estará disponible hasta que el tetrominó que se movió fuera del espacio de espera se bloquee.

#### Puntaje

  

El puntaje se conseguirá al completar filas, hacer [combos](https://tetris.wiki/Combo), hacer un [perfect clear](https://tetris.wiki/Perfect_clear), hacer soft drop o hard drop. El puntaje también depende del nivel actual. Los puntajes serán:

  

-   Completar 1 fila: 100 x nivel
    
-   Completar 2 filas: 300 x nivel
    
-   Completar 3 filas: 500 x nivel
    
-   Completar 4 filas (“hacer un Tetris”): 800 x nivel

-   Completar 1 fila con perfect clear: 800 x nivel
    
-   Completar 2 filas con perfect clear: 1200 x nivel
    
-   Completar 3 filas con perfect clear: 1800 x nivel
    
-   Completar 4 filas con perfect clear: 2000 x nivel

-   Combo: 50 × combo count × nivel
    
-   Soft drop: 1 punto (por cada movimiento)
    
-   Hard drop: 2 x fila (altura de la caída)