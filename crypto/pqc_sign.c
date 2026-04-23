#include <oqs/oqs.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define SIG_ALG "Dilithium2"

static OQS_SIG *sig = NULL;
static uint8_t *public_key = NULL;
static uint8_t *secret_key = NULL;

void init_keys() {
    if (sig != NULL) return;

    sig = OQS_SIG_new(SIG_ALG);
    if (sig == NULL) return;

    public_key = malloc(sig->length_public_key);
    secret_key = malloc(sig->length_secret_key);

    if (public_key == NULL || secret_key == NULL) return;

    if (OQS_SIG_keypair(sig, public_key, secret_key) != OQS_SUCCESS) {
        free(public_key);
        free(secret_key);
        public_key = NULL;
        secret_key = NULL;
    }
}

void pq_sign(const uint8_t *message, size_t message_len, uint8_t *signature) {
    init_keys();

    if (sig == NULL || secret_key == NULL) return;

    size_t sig_len = 0;

    OQS_SIG_sign(
        sig,
        signature,
        &sig_len,
        message,
        message_len,
        secret_key
    );
}

int pq_verify(const uint8_t *message, size_t message_len, uint8_t *signature) {
    init_keys();

    if (sig == NULL || public_key == NULL) return 0;

    return OQS_SIG_verify(
        sig,
        message,
        message_len,
        signature,
        sig->length_signature,
        public_key
    ) == OQS_SUCCESS;
}

size_t pq_sig_length() {
    init_keys();

    if (sig == NULL) return 0;

    return sig->length_signature;
}