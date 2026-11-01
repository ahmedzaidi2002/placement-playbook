# curl scripts

Start the server first (`npm start` in the project folder), then in a second terminal:

| Script | What it does | Reads from arguments.json |
|---|---|---|
| `./01_register_user.sh` | register a user | `register` |
| `./02_login.sh` | log in, save the token to `.token` | `login` |
| `./15_create_promo_code.sh` | create a promo code | `createPromo` |
| `./16_validate_promo_code.sh` | validate a code for an event and quantity | `validatePromo` |
| `./17_create_order.sh` | place an order with a code (counts one use) | `createOrder` |
| `./18_delete_promo_code.sh` | soft-delete a code | `deletePromo` |
| `./19_list_promo_codes.sh` | list all codes, deleted ones too | none |

Each script prints the request, the response body, and the HTTP status on the last line.
If you get "Permission denied", run `chmod +x *.sh` once.
