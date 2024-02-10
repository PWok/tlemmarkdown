
Znamy już wiele funkcji służących do generowania danych losowych oraz sposób na wpływanie na wewnętrzny stan generatora – funkcję `seed()`.  Pozwala to nam na wywoływanie wielu ciekawych efektów związanych z losowością. Ale nagle dzieje się rzecz straszna! Wesoło sobie zmienialiśmy stan generatora w naszym programie, ale okazuje się, że inne jego części związane z losowością przestały działać. Co się dzieje?! Przyczyną może być to, że wszystkie moduły w jednym skrypcie Pythona wykorzystują tą samą instancję modułu `random`. Oznacza to, że jeżeli korzystamy z jakiegoś modułu, który samemu też wykorzystuje funkcje zdefiniowane w module `random` może się okazać, że często ustawiając stan generatora funkcję `seed()` wpłyniemy negatywnie na jakość generowanych przez ten zewnętrzny moduł danych. Na szczęście istnieje rozwiązanie – utworzenie niezależnej instancji generatora. Umożliwia nam to zdefiniowana klasa `random.Random`. Możemy stworzyć taką instancję w następujący sposób:
```python
from random import Random
inst = Random()
```
i wykorzystać ją np. w następujący sposób:

```python
inst.seed(7)
inst.randrange(857)
>>> 331
inst.seed(7)
inst.randrange(857)
>>> 331

inst.seed(7)
x = ["Ala", "ma", "Pythona"]
inst.shuffle(x)
x
>>> ["Pythona", "Ala", "ma"]
```
Każda instancja implementuje dokładnie te same metody (funkcje) co moduł `random`, a jeżeli przy tworzeniu instancji generatora do konstruktora `Random()` przekażemy argument to zostanie on wykorzystany jako ziarno
