#include <stdlib.h>
const int false = 0;
const int true = 1;

// Linked List Struct for information of collected phrases
struct _LinkedListStruct  {
  int *phrase;
  long *ids;
  int num_ids;
  struct _LinkedListStruct*next;
} _LLS;



// Phrase counter without respecting sentences
struct _LinkedListStruct *_pcounter(
              int *mess_len, // array storing the number words of each message
              long num_messages,
              int **messages, // large 2d-array of messages
              int **mark, // 2d-array of bool for each word in all messages
              long *ids, int phr_len)
{
  // Define head and current of linked list 
  struct _LinkedListStruct *collected_head = NULL;
  struct _LinkedListStruct *collected_current = collected_head;


  /***** calculate all possible phrases in text with phr_len *****/
  // Number of possible phrases
  long poss_num_phr = 0;
  for (long mess=0; mess<num_messages; mess++) //messages of this mess_length
    if (mess_len[mess] - phr_len + 1 > 0)
      poss_num_phr += mess_len[mess] - phr_len + 1;
  //Array of pointers for storing (first-word-)address of collected phrases
  int **phrases = (int **)malloc(poss_num_phr * sizeof(int*));
  // Number of collected phrases
  long num_phrases = 0;
  for (long mess=0; mess<num_messages; mess++) //loop over all messages
  {
    int poss_num_mess_phr = mess_len[mess] - phr_len + 1;
    for (int i=0; i<poss_num_mess_phr; i++) // loop over possible phrases
    {
      int already_in_phrases = false;
      for (long ii=0; ii<num_phrases; ii++)
      {
        int equal = true;
        for (int j=0; j<phr_len; j++)
          equal *= (messages[mess][i+j] == *(*(phrases+ii)+j)); 
        if (equal)
          already_in_phrases = true;
      }

      if (!already_in_phrases)
      {
        phrases[num_phrases] = &(messages[mess][i]); //add to possible phrases
        num_phrases++;
      }
    }
  }


  /***** search all possible phrases in all messages for recurrence*****/
  for (long p=0; p<num_phrases; p++) // loop over all possible phrases
  {
    int occurrence = 0;
    long count_ids[num_messages];//(too large) array for collecting ids
    int c_idx = 0; //index of collected ids
    for (long mess=0; mess<num_messages; mess++) //messages of this mess_length
    {
      // check if phrase already counted in this message
      int already_counted_in_t = false;
      int poss_num_phr = mess_len[mess] - phr_len + 1;
      for (int i=0; i<poss_num_phr; i++) //loop over all phrases in this mess
      {
        int equal = true;
        for (int j=0; j<phr_len; j++) // and compare with this phrase
          if (!(messages[mess][i+j] == *(*(phrases+p)+j)))
            equal = false;
        
        if (equal)
        {
          occurrence++;
          int marked = true; // check if phrase occurence is completely marked
          for (int j=0; j<phr_len; j++)
            marked *= (mark[mess][i+j]);
          
          if (!marked && !already_counted_in_t)
          {
            count_ids[c_idx] = ids[mess]; //add this occurence (i.e. message id)
            c_idx++;
            already_counted_in_t = true;
          }
        }
      }
    }

    
    /***** Transfer collected phrases and ids to results (linked list) *****/
    // only collect phrase if it appears more than once
    if (occurrence >= 2 && c_idx >= 1)
    {
      struct _LinkedListStruct *phrase_struct = malloc(sizeof(_LLS));
      phrase_struct->phrase = (int *)malloc(phr_len * sizeof(int));
      for (int j=0; j<phr_len; j++)
        phrase_struct->phrase[j] = *(*(phrases+p)+j);
      phrase_struct->num_ids = c_idx;
      phrase_struct->ids = (long *)malloc(c_idx * sizeof(long));
      for (int c=0; c<c_idx; c++)
        phrase_struct->ids[c] = count_ids[c];
      phrase_struct->next = NULL;
      if (collected_head == NULL)  {
        collected_head = phrase_struct;
        collected_current = collected_head;
      }
      else  {
        collected_current->next = phrase_struct;
        collected_current = collected_current->next;
      }
    }
  }


  /***** Mark all occurences of collected phrases *****/
  struct _LinkedListStruct *collected = collected_head;
  while (collected != NULL) // loop over collected phrases
  {
    for (long mess=0; mess<num_messages; mess++) // loop over all messages
    {
      int poss_num_phr = mess_len[mess] - phr_len + 1;
      for (int i=0; i<poss_num_phr; i++) // loop over poss. phrases in message 
      {
        int equal = true;
        for (int j=0; j<phr_len; j++) // collected phrase in message?
          if (!(messages[mess][i+j] == collected->phrase[j]))
            equal = false;
        
        if (equal)
          for (int j=0; j<phr_len; j++)
            mark[mess][i+j] = true;
      }
    }
    collected = collected->next;
  }
  return collected_head;
}



// Phrase counter with respecting sentences
struct _LinkedListStruct *_pcounter_sent(
              int *mess_len, //array storing the number of sentences per message
              int *sent_len, //array storing the number words of each sentence
              long num_messages, long num_sentences,
              int **sentences, // large array of sentences
              int **mark, // array of bool for for every word in all sentences
              long *ids, int phr_len)
{
  // Define head and current of linked list 
  struct _LinkedListStruct *collected_head = NULL;
  struct _LinkedListStruct *collected_current = NULL;

  
  /***** calculate all possible phrases in text with phr_len *****/
  // Number of possible phrases
  long poss_num_phr = 0;
  for (long sent=0; sent<num_sentences; sent++) //messages
    if (sent_len[sent] - phr_len + 1 > 0)
      poss_num_phr += sent_len[sent] - phr_len + 1;
  //Array of pointers for storing (first-word-)address of collected phrases
  int **phrases = (int **)malloc(poss_num_phr * sizeof(int*));
  // Index for collected phrases
  long num_phrases = 0;
  for (long sent=0; sent<num_sentences; sent++) // loop over all sentences
  {
    int poss_num_mess_phr = sent_len[sent] - phr_len + 1;
    for (int i=0; i<poss_num_mess_phr; i++) // loop over possible phrases
    {
      int already_in_phrases = false;
      for (long ii=0; ii<num_phrases; ii++)
      {
        int equal = true;
        for (int j=0; j<phr_len; j++)
          equal *= (sentences[sent][i+j] == *(*(phrases+ii)+j));
        if (equal)
          already_in_phrases = true;
      }

      if (!already_in_phrases)
      {
        phrases[num_phrases] = &(sentences[sent][i]); // add to possible phrases
        num_phrases++;
      }
    }
  }


  /***** search all possible phrases in all sentences for recurrence*****/
  for (long p=0; p<num_phrases; p++)
  {
    int occurrence = 0;
    long count_ids[num_messages];//(too large) array for collecting ids
    int c_idx = 0; //index of collected ids 
    int sent = 0; // loop over sentences (via messages)
    for (long mess=0; mess<num_messages; mess++)
    {
      // check if phrase already counted in this sentence
      int already_counted_in_t = false;
      int max_num_sent = sent + mess_len[mess];
      while(sent<max_num_sent)
      {
        int poss_num_phr = sent_len[sent] - phr_len + 1;
        for (int i=0; i<poss_num_phr; i++) //loop over all phrases in this sent
        {
          int equal = true;
          for (int j=0; j<phr_len; j++) // and compare with this phrase
            if (!(sentences[sent][i+j] == *(*(phrases+p)+j)))
              equal = false;
          
          if (equal)
          {
            occurrence++;
            int marked = true; // check if phrase occurence is completely marked
            for (int j=0; j<phr_len; j++)
              marked *= (mark[sent][i+j]);
            
            if (!marked && !already_counted_in_t)
            {
              count_ids[c_idx] = ids[mess]; //add this occurence (i.e. mess id)
              c_idx++;
              already_counted_in_t = true;
            }
          }
        }
        sent++;
      }
    }
    
  
    /***** Transfer collected phrases and ids to results (linked list) *****/
    // only collect phrase if it appears more than once
    if (occurrence >= 2 && c_idx >= 1)
    {
      // collected_phrases.append(this_phrase)
      struct _LinkedListStruct *phrase_struct = malloc(sizeof(_LLS));
      phrase_struct->phrase = (int *)malloc(phr_len * sizeof(int));
      for (int j=0; j<phr_len; j++)
        phrase_struct->phrase[j] = *(*(phrases+p)+j);
      phrase_struct->num_ids = c_idx;
      phrase_struct->ids = (long *)malloc(c_idx * sizeof(long));
      for (int c=0; c<c_idx; c++)
        phrase_struct->ids[c] = count_ids[c];
      phrase_struct->next = NULL;
      if (collected_head == NULL)  {
        collected_head = phrase_struct;
        collected_current = collected_head;
      }
      else  {
        collected_current->next = phrase_struct;
        collected_current = collected_current->next;
      }
    }
  }

  
  /***** Mark all occurences of collected phrases *****/
  struct _LinkedListStruct *collected = collected_head;
  while (collected != NULL) // loop over collected phrases
  {
    for (int sent=0; sent<num_sentences; sent++) // loop over all sentences
    {
      int poss_num_phr = sent_len[sent] - phr_len + 1;
      for (int i=0; i<poss_num_phr; i++) //loop over poss. phrases in sentence
      {
        int equal = true;
        for (int j=0; j<phr_len; j++) // collected phrase in sentence?
          if (!(sentences[sent][i+j] == collected->phrase[j]))
            equal = false;
        
        if (equal)
          for (int j=0; j<phr_len; j++)
            mark[sent][i+j] = true;
      }
    }
    collected = collected->next;
  }
  return collected_head;
}
