
void nothing() {
	printf("nothing()\n");
}

void nothing2(int a) {
	printf("nothing2(%d)\n", a);
}

int add(int a, int b) {
	return a+b;
}

float addf(float a, float b) {
	return a+b;
}

char* reverse(char* a) {
	int i;
	char* ret = malloc(strlen(a));
	if (!ret) return ret;
	for (i = strlen(a)-1; i >= 0; i--) 
		ret[i] = a[i];
	return ret;
}
