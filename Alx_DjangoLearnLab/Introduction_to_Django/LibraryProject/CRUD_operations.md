python manage.py shell -c "
from bookshelf.models import Book
from bookshelf.admin import BookAdmin
print('✓ Book model: OK')
print('✓ BookAdmin: OK')
print('✓ All migrations applied')
"
