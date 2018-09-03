/* $RCSfile$Revision$Date$
 *------------------------------------------------------------------------
 *
 * lib.table.h -- This file contains definitions for hash table routines.
 *
 *------------------------------------------------------------------------
 */

#ifndef _LIB_TABLE_H_
#define _LIB_TABLE_H_

#define RESETFACTOR        2
#define RESETLIMIT         1.5
#define DEFAULT_SLOTS      16

struct hLinks {
    struct hLinks *fwPtr;
    struct hLinks *bwPtr;
};

typedef struct hLinks hLinks;

typedef struct hEnt {
    hLinks links;            /* slot queue */
    int     *hData;           
    char    *keyname;        
} hEnt;


typedef struct hTab {
    hLinks *slotPtr;          /* Pointer to an array of slots */
    int     numEnts;           /* Number of entries in the table. */
    int     size;              /* Actual size of array. */
} hTab;


typedef struct sTab {
    hTab     *tabPtr;     
    int      nIndex;            
    hEnt     *hEntPtr;         
    hLinks   *hList;          
} sTab;

#define HTAB_ZERO_OUT(HashTab) \
{ \
    (HashTab)->numEnts = 0; \
    (HashTab)->size = 0; \
}

#define HTAB_NUM_ELEMENTS(HashTab) (HashTab)->numEnts

#define FOR_EACH_HTAB_ENTRY(Key, Entry, HashTab) \
{ \
    sTab __searchPtr__; \
    (Entry) = h_firstEnt_((HashTab), &__searchPtr__); \
    for ((Entry) = h_firstEnt_((HashTab), &__searchPtr__); \
         (Entry); (Entry) = h_nextEnt_(&__searchPtr__)) { \
	 (Key)   = (char *) (Entry)->keyname;

#define FOR_EACH_HTAB_ENTRY_WITHOUT_KEY(Entry, HashTab) \
{ \
    sTab __searchPtr__; \
    (Entry) = h_firstEnt_((HashTab), &__searchPtr__); \
    for ((Entry) = h_firstEnt_((HashTab), &__searchPtr__); \
         (Entry); (Entry) = h_nextEnt_(&__searchPtr__)) {

#define END_FOR_EACH_HTAB_ENTRY  }}

#define FOR_EACH_HTAB_DATA(Type, Key, Data, HashTab) \
{ \
    sTab __searchPtr__; \
    hEnt *__hashEnt__; \
    __hashEnt__ = h_firstEnt_((HashTab), &__searchPtr__); \
    for (__hashEnt__ = h_firstEnt_((HashTab), &__searchPtr__); \
         __hashEnt__; __hashEnt__ = h_nextEnt_(&__searchPtr__)) { \
        (Data) = (Type *) __hashEnt__->hData; \
	(Key)   = (char *) __hashEnt__->keyname;

#define END_FOR_EACH_HTAB_DATA  }}

typedef void       (*HTAB_DATA_DESTROY_FUNC_T)(void *);

extern void        insList_(hLinks *, hLinks *);
extern void        remList_(hLinks *);
extern void        initList_(hLinks *);
extern void        h_initTab_(hTab *, int);
extern void        h_freeTab_(hTab *, void (*destroy)(void *));
extern int         h_TabEmpty_(hTab *);
extern void        h_delTab_(hTab *);
extern hEnt *      h_getEnt_(hTab *, const char *);
extern hEnt *      h_addEnt_(hTab *, const char *, int *);
extern hEnt *      lh_addEnt_(hTab *, char *, int *);
extern void        h_delEnt_(hTab *, hEnt *);
extern void        h_rmEnt_(hTab *, hEnt *);
extern hEnt *      h_firstEnt_(hTab *, sTab *);
extern hEnt *      h_nextEnt_(sTab *);
extern void        h_freeRefTab_(hTab *);
extern void        h_delRef_(hTab *, hEnt *);
extern void       h_dupTab_(hTab **, hTab *, void *(*cpFunc)(void *));
#endif




