#Code for perturbation and generating importance scores

def perturb_sentence(sentence, tokenizer):
    """Perturb the input sentence by masking out one word at a time."""
    words = tokenizer.tokenize(sentence)
    perturbed_sentences = []

    for i in range(len(words)):
        perturbed = words[:i] + ['[MASK]'] + words[i+1:]
        perturbed_sentences.append(tokenizer.convert_tokens_to_string(perturbed))
    
    return perturbed_sentences

def compute_influences(sentence, clf, tokenizer, biobert, get_specific_token_embeddings):
    """Compute the influence of each word on the classifier's prediction."""
    original_confidences=[]
    perturbed_confidences=[]
    perturbed_sentences = perturb_sentence(sentence, tokenizer)
    original_embedding = get_specific_token_embeddings(sentence).reshape(1, -1)
    original_confidence = clf.predict_proba(original_embedding)[0][1]
    original_confidences.append(original_confidence)

    influences = []
    org_probs = []
    perturbed_probs = []
    for perturbed in perturbed_sentences:
        perturbed_embedding = get_specific_token_embeddings(perturbed).reshape(1, -1)
        perturbed_confidence = clf.predict_proba(perturbed_embedding)[0][1]
        perturbed_confidences.append(perturbed_confidence)
        
        influence=(max(perturbed_confidence-0.5, original_confidence-0.5, 0))*(original_confidence-perturbed_confidence)
        #influence = abs(original_confidence - perturbed_confidence)
        #influence =  perturbed_confidence - original_confidence
        influences.append(influence)
        org_probs.append(original_confidence)
        perturbed_probs.append(perturbed_confidence)
        

    return influences, org_probs, perturbed_probs

def rank_words_by_influence(sentence, influences, tokenizer, org_probs, perturbed_probs):
    #print(sentence)
    """Rank words by their influence."""
    words = tokenizer.tokenize(sentence)
    all_words = []
    all_influence_scores = []
    all_org_prob_scores = []
    all_perturbed_prob_scores = []
    importance = []
    org_prob_importance = []
    perturbed_prob_importance = []
    word = ""
    old_word = None
    for influence, org_prob, perturbed_prob, token in zip(influences, org_probs, perturbed_probs, words):
        if len(token) == 1:
            continue
        if token.startswith("#"):
            new_token = token.replace('#', '')
            word += new_token.strip()
            importance.append(influence)
            org_prob_importance.append(org_prob)
            perturbed_prob_importance.append(perturbed_prob)
        else:
            if old_word is None:
                all_words.append(word)
                all_influence_scores.append(influence)
                all_org_prob_scores.append(org_prob)
                all_perturbed_prob_scores.append(perturbed_prob)
            else:
                if old_word.startswith("#"):
                    all_words.append(word)
                    word = "" + token
                    influence_score = sum(importance) / len(importance)
                    org_prob_score = sum(org_prob_importance) / len(org_prob_importance)
                    perturbed_prob_score = sum(perturbed_prob_importance) / len(perturbed_prob_importance)
                    all_influence_scores.append(influence_score)
                    all_org_prob_scores.append(org_prob_score)
                    all_perturbed_prob_scores.append(perturbed_prob_score)
                else:
                    all_words.append(old_word)
                    word = "" + token
                    importance.append(influence)
                    org_prob_importance.append(org_prob)
                    perturbed_prob_importance.append(perturbed_prob)
                    all_influence_scores.append(old_imp)
                    all_org_prob_scores.append(old_org_prob)
                    all_perturbed_prob_scores.append(old_perturbed_prob)
            old_word = token
            old_imp = influence
            old_org_prob = org_prob
            old_perturbed_prob = perturbed_prob
    
    ranked_words = [word for _, word in sorted(zip(all_influence_scores, all_words), reverse=True)]
    return ranked_words, all_words, all_influence_scores, all_org_prob_scores, all_perturbed_prob_scores


def aggregate_word_importance(words, imp_scores, org_prob_scores, perturbed_prob_scores):
    """Aggregate scores for words into a single dictionary."""
    word_importance = {}

    for word, imp_score, org_prob_score, perturbed_prob_score in zip(words, imp_scores, org_prob_scores, perturbed_prob_scores):
        if len(word)>2:
            if word in word_importance:
                # Update existing entry with max scores
                word_importance[word] = [max(word_importance[word][0], imp_score),
                                         max(word_importance[word][1], org_prob_score),
                                         max(word_importance[word][2], perturbed_prob_score)]
            else:
                # Create new entry for the word
                word_importance[word] = [imp_score, org_prob_score, perturbed_prob_score]

    return word_importance


def save_word_importance_to_file(word_importance, row, filename='word_imp_sc_test_data_CDR_trained_new.tsv'):
    """Save word importance scores to a file."""
    with open(filename, 'a') as file:
        for k, v in word_importance.items():
            # Write index, id1, id2, word, and importance score
            file.write(f"{row['index']}\t{row['id1']}\t{row['id2']}\t{k}\t{v[0]}\t{v[1]}\t{v[2]}\n")


def interpretation(row, clf, tokenizer, biobert, get_specific_token_embeddings):
    sentence = row['sentence']
    
    influences, org_probs, perturbed_probs = compute_influences(sentence, clf, tokenizer, biobert, get_specific_token_embeddings)
    ranked, words, imp_scores, org_prob_scores, perturbed_prob_scores = rank_words_by_influence(sentence, influences, tokenizer, org_probs, perturbed_probs)
    ranked = [i for i in ranked if len(i) > 1]
    #print("Words ranked by influence:", ranked)
    word_importance = aggregate_word_importance(words, imp_scores, org_prob_scores, perturbed_prob_scores)
    save_word_importance_to_file(word_importance, row)
    return ranked, word_importance
