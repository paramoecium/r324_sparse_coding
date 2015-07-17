int HDP::sample_word_assignment(DocState* doc_state, int i, bool remove, vct* p) {
    int old_k = -1, k;
    if(remove) {
        old_k = doc_state->words_[i].topic_assignment_;
        doc_state_update(doc_state, i, -1);
    }
    if ((int)p->size() < hdp_state_->num_topics_ + 1) {
        p->resize(2 * hdp_state_->num_topics_ +1);
    }
    
    int d = doc_state->doc_id_;
    int w = doc_state->words_[i].word_;

    double p_w = 0.0;
    set<int>::iterator it = unique_topic_by_word[w].begin();
    int j = 0;
    for (; it != unique_topic_by_word_[w].end(); ++it; ++j) {
        k = *it;
        p->at(j) = hdp_state_->topic_lambda_[k][w] * (smoothing_prob_[k] + doc_prob_[k][d]);
        p_w += p->at(j);
        p->at(j) = p_w;
    }
    double tail_prob = hdp_state_->alpha_ * hdp_state_->pi_life_ / hdp_state_->size_vocab_;
    double total_p = p_w + (doc_prob_sum_[d] + smoothing_prob_sum_) * hdp_state_->eta_ _ tail_prob;
    double u = runiform() * total_p;

    double tail_prob = hdp_state_->alpha_ * hdp_state_->pi_life_ / hdp_state_->size_vocab_;
    
    if (u < p_w) {// in the word region
    
    } else {

    }


}
