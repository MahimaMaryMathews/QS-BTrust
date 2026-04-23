void pq_sign(const unsigned char* message, size_t message_len, unsigned char* signature);
int pq_verify(const unsigned char* message, size_t message_len, unsigned char* signature);