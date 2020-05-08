#include "aes.h"

void encrypt(unsigned char * msg, unsigned char * key)
{

  unsinged char state[16];
  for (int i = 0; i < 16; i++)
  {
    state[i] = msg[i];
  }

  unsigned char expandedKey[176];
  keyExpansion(key, expandedKey);
  addRoundKey(state, key);

  for (int i = 0; i < NUM_ROUNDS; i++)
  {
    subBytes(state);
    shiftRows(state);
    mixColumns();
    addRoundKey(state, expandedKey + (16 * (i + 1)));
  }

  subBytes(state);
  shiftRows(state);
  addRoundKey(state, expandedKey + 160);

  for (int i = 0; i < 16; i++)
  {
    msg[i] = state[i];
  }
}

void keyExpansion(unsigned char * inputKey, unsigned char * expandedKeys)
{
  for (int i = 0; i < 16; i++)
  {
    expandedKeys[i] = inputKey[i];
  }

  int bytesGenerated = 16;
  int rconIteration = 1;
  unsigned char tmp[4];

  while (bytesGenerated < 176)
  {
    for (int i = 0; i < 4; i++)
    {
      tmp[i] = expandedKeys[i + bytesGenerated - 4];
    }

    if (bytesGenerated % 16 == 0)
    {
      keyExpansionCore(tmp, rconIteration++);
    }

    for (unsigned char j = 0; j < 4; j++)
    {
      expandedKeys[bytesGenerated] = expandedKeys[bytesGenerated - 16] ^ tmp[j];
      bytesGenerated++;
    }
  }
}

void keyExpansionCore(unsigned char * in, unsigned char i)
{
  unsigned int * tmp = (unsigned int *) in;
  *tmp = (*tmp >> 8) | ((*tmp & 0xff) << 24);

  in[0] = sbox[in[0]];
  in[1] = sbox[in[1]];
  in[2] = sbox[in[2]];
  in[3] = sbox[in[3]];

  in[0] ^= rcon[i];
}

void subBytes(unsigned char * state)
{
  for (int i = 0; i < 16; i++)
  {
    state[i] = sbox[state[i]];
  }
}

void shiftRows(unsigned char * state)
{
  unsigned char tmp[16];

	tmp[0] = state[0];
	tmp[1] = state[5];
	tmp[2] = state[10];
	tmp[3] = state[15];

  tmp[4] = state[4];
	tmp[5] = state[9];
	tmp[6] = state[14];
	tmp[7] = state[3];

  tmp[8] = state[8];
	tmp[9] = state[13];
	tmp[10] = state[2];
	tmp[11] = state[7];

  tmp[12] = state[12];
	tmp[13] = state[1];
	tmp[14] = state[6];
	tmp[15] = state[11];

  for (int i = 0; i < 16; i++)
  {
    state[i] = tmp[i];
  }
}

void mixColumns(unsigned char * state)
{
  unsigned char tmpState = *state;
  int i = 0;
  int j;

  while (i < 4)
  {
  	tmpState[i] = gf_mul[state[i]][0] ^ gf_mul[state[i+4]][1] ^ state[8+i] ^ state[12+i];
  	tmpState[4+i] = state[i] ^ gf_mul[state[4+i]][0] ^ gf_mul[state[8+i]][1] ^ state[12+i];
  	tmpState[8+i] = state[i] ^ state[4+i] ^ gf_mul[state[8+i]][0] ^ gf_mul[state[12+i]][1];
  	tmpState[12+i] = gf_mul[state[i]][1] ^ state[4+i] ^ state[8+i] ^ gf_mul[state[12+i]][0];
  	i++;
  }

	for (j=0; j<16; j++)
  {
		state[i] = tmpState[i];
  }
}

void addRoundKey(unsigned char * state, unsigned char * roundKey)
{
  for (int i = 0; i < 16; i++)
  {
    state[i] ^= roundKey[i];
  }
}
