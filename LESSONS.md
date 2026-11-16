# The commands from each lesson

Every command typed in the lesson videos, in order. Run them from the root of
this repository, after the setup in README.md.

## 3.1.3 Starting and verifying a practice orders site

```bash
cd getting-started
python3 app.py &
curl http://127.0.0.1:8000/health
curl -u alice:wonderland http://127.0.0.1:8000/orders
kill %1
```

## 3.1.4 Checking and limiting who can read a file

```bash
cd file-permissions
ls -l customers.csv
chmod 600 customers.csv
ls -l customers.csv
```

## 3.1.5 Checking that a file hasn't changed

```bash
cd file-integrity
sha256sum customers.csv
sha256sum customers.csv > customers.sha256
sha256sum -c customers.sha256
echo "Eve Lindqvist,Oslo,1" >> customers.csv
sha256sum -c customers.sha256
```

## 3.3.2 Listing a web app's entry points

```bash
cd entry-points
grep -n "if self.path" app.py
python3 app.py &
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/orders
kill %1
```

## 3.4.2 Viewing another user's order

```bash
cd another-users-order
python3 app.py &
curl -u alice:wonderland http://127.0.0.1:8000/orders
curl -u alice:wonderland http://127.0.0.1:8000/orders/2
kill %1
```

## 3.4.3 Adding the missing access check

```bash
cd access-check
grep -n -B1 -A1 "not your order" app.py
python3 app.py &
curl -i -u alice:wonderland http://127.0.0.1:8000/orders/2
kill %1
```

## 3.4.4 Verifying the access check

```bash
cd verify-access
python3 app.py &
curl -i -u alice:wonderland http://127.0.0.1:8000/orders/1
curl -i -u alice:wonderland http://127.0.0.1:8000/orders/2
curl -i -u bob:builder http://127.0.0.1:8000/orders/2
curl -i http://127.0.0.1:8000/orders/2
kill %1
```
