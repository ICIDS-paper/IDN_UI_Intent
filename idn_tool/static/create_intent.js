

$(document).ready(function() {
$('#media').on('change',function(){
    if( $(this).val()==="3.fiction"){
    $(this).parent(".form-group").next().removeClass("hidden");
    }
    else{
    $(this).parent(".form-group").next().addClass("hidden");
    }
});


});



$(document).ready(function() {
$('#narrative_type').on('change',function(){
    if( $(this).val()==="2.short_story"){
    $(this).parent(".form-group").next().removeClass("hidden");
    }
    else{
    $(this).parent(".form-group").next().addClass("hidden");
    }
});


});


$(document).ready(function() {
$('#modality').on('change',function(){
    if( $(this).val()==="2.text"){
    $(this).parent(".form-group").next().removeClass("hidden");
    }
    else{
    $(this).parent(".form-group").next().addClass("hidden");
    }
});


});

$(document).ready(function() {
$('#modality').on('change',function(){
    if( $(this).val()==="3.text+visual"){
    $(this).parent(".form-group").next().next().removeClass("hidden");
    }
    else{
    $(this).parent(".form-group").next().next().addClass("hidden");
    }
});


});


$(document).ready(function() {
$('#background').on('change',function(){
    if( $(this).val()==="Yes"){
    $('#BackgroundStoryModal').modal('show');
    }
    if( $(this).val()==="No"){
    var formGroup = document.querySelector('.form-group');
    formGroup.classList.add('hidden');
    }
});


});



document.addEventListener('DOMContentLoaded', function() {

    // Get the button and textarea elements
    var generateButton = document.querySelector('.generate-background');
    var refineButton = document.querySelector('.refine-background');
    var submitButton = document.querySelector('.submit-background');
    var backgroundStoryTextarea = document.getElementById('background-story');
    var authorFeedbackTextarea = document.getElementById('author-feedback');
    var formGroup = document.querySelector('.form-group');


    // Add event listener to the generate button
    generateButton.addEventListener('click', function() {
      // Hardcoded text for demonstration purposes
      var hardcodedText = "In a bizarre twist that could only be conceived in the absurdist world, Gregor Samsa, a scrupulous and diligent traveling salesman from a nondescript European city of the early 20th century, awakens one surreal morning with his humanity ensnared within the grotesque exoskeleton of a monstrous insect. This transformation, absurd as it may be, lays the foundation for a poignant exploration of the frailty of human relationships and the alienation that accompanies profound change. The Samsa family's once mundane existence, confined within the drab walls of their aging apartment, spirals into chaos as their primary breadwinner becomes the object of repulsion and mounting financial strain. Gregors desperate attempts to adjust to his new condition and cling to any vestiges of human contact with his family reveal the overarching theme: the struggle to maintain one’s identity in the face of incomprehensible transformation. The gradual shift in familial dynamics hinges upon the motifs of metamorphosis and alienation—which are key motivators in guiding interactive choices. In addition to Gregor, the character profiles of the Samsa family members emerge as driven by conflicting emotions and economic pressure. Grete, Gregor's devoted sister, initially displays compassion, only for it to crumble under the weight of responsibility and disillusionment. The once-defeated Mr. Samsa finds an antiquated vigor in the necessity to return to work, replacing his son as the provider and thus altering his stance from dependency to authoritative resentment. Meanwhile, Mrs. Samsa tiptoes the line between maternal love and overwhelming dismay, a symbol of the fragile balance each character must navigate.As participants delve into this interactive narrative, they will encounter main events that deepen the emotional resonance of Gregor's plight. Subplots marbled within the central story include exploration of the family's past financial decisions, unwrapping mysteries of their prior misfortunes that perhaps led to the symbolic crushing burden Gregor felt pre-transformation. A key event will be the semblance of hope when a trio of boarders is taken in—a decision ripe with interactive opportunities as it introduces new dynamics and strains. Interactive objects are woven throughout the story: the typewriter symbolizing Gregor’s lost voice, the violin once played by Grete that becomes an eerie reminder of lost talents and aspirations, and the key to Gregor’s room, an object of control over his confinement. These items and more not only engage participants with their symbolic representations but also serve as catalysts for advancing the plot and revealing deeper character facets. Locations within the Samsa's struggling household are meticulously crafted to mirror the internal chaos - Gregor's room, simultaneously a sanctuary and a prison; the kitchen, a battlefield of familial responsibilities; the living room turned boarding hall, where the drama of external perception plays out. Each space presents a unique stage for unraveling the intricacies hidden within the absurdities, engaging the participant in a domestic landscape filled with secrets and psychological entanglements. Throughout the story, the tangle of human emotion and absurdity invites individuals to not only witness but interact within the surreal and allegorical realm that questions the nature of change and the human condition. The narrative thus becomes a remarkable tapestry of choice and consequence, wrapped in the shroud of the absurdist genre, that unfolds within the grip of the protagonist's monstrous transformation.";
      // Populate the textarea with the hardcoded text
      backgroundStoryTextarea.value = hardcodedText;

    });


      // Add event listener to the refine button
  refineButton.addEventListener('click', function() {
    // Get the content from the author's feedback textarea
    var feedbackContent = authorFeedbackTextarea.value;
    //add a custom value which came from the API of Alireze
    var feedbackContent = "In the claustrophobic milieu of an undistinguished Central European city, during the disquieting era of the 1920s, Gregor Samsa, a meticulously assiduous traveling salesman, is jolted into consciousness on one bewildering morning to find his humanity imprisoned within the grotesque carapace of an insectile behemoth. This predicament, striking in its absurdity, becomes a conduit for a profound interrogation into the fragility of human connections and the estrangement birthed by inconceivable change. Henceforth, the drab, decaying walls of the Samsa family abode become a theater of disarray; their once dull life is upended, their main source of income now an entity of aversion and an anchor to financial despondency. Delving deeply into the hues of cultural desolation and existential angst that color this time, the story reveals Gregor’s frantic efforts to preserve his identity amidst his baffling metamorphosis. These struggles strike a chord parallel to the brooding works of Dostoevsky, welding the overarching themes of alienation and selfhood to drive interactive story choices. As Gregor’s forlorn hope for empathy from his kin wanes, the family dynamics warp, elucidating the motifs of transformation and isolation. Grete, Gregor’s dear sister, with whom he shared a genuine and unwavering bond, blooms into prominence. Their relationship, anchored by trust and mutual respect, once saw Gregor as the encourager of Grete’s budding talent with the violin—a symbol of her dreams and possibilities. In the unfolding narrative, she rallies an initial wave of compassion for her transmogrified brother, nursing a fragile hope in her heart. Yet, as the responsibilities and disillusionment fester, Grete’s patience and empathy erode, hardening into a bedrock of resentment and repulsion, expunged of her former affection. Their once-submissive father rediscovers a semblance of his bygone vitality, as economic necessity thrusts him back into the workforce, usurping Gregor's role as the provider. This shift metamorphoses Mr. Samsa’s attitude from one of reliance to a bitter authoritarian. Concurrently, Mrs. Samsa wavers on the precipice of maternal devotion and her own rising hysteria, representing the tenuous equilibrium each family member must traverse. Participants are drawn into a narrative pulsating with Gregor’s lonely struggle against his monstrous fate, side stories that peel back layers on the family's prior financial blunders, and the symbolic enormity of the debt that Gregor bore before his surreal affliction. A fleeting promise of financial reprieve surfaces with the introduction of a trio of boarders, a plot point replete with choices that examine new constraints and dynamics. Interactive symbols lace the story: a typewriter signifying Gregor's muted voice, the violin now an eerie relic of Grete's forsaken aspirations, and the key to Gregor's room, a dominion over his seclusion. These objects are not mere playthings but act as vessels through which the story’s depth and the characters’ complexities are divulged. The household's meticulously designed settings reflect the internal tumult: Gregor's room, his refuge-turned-dungeon; the kitchen, where the battle of domesticity ensues; the living room, transformed into a boarding sanctuary, acting as both stage and cage for the unfolding societal judgment. Each enclave offers distinct challenges, inviting the participant to disentangle the nuanced intricacies tucked within the absurd. The story weaves an intricate web of emotive force and surrealism, compelling participants to navigate a world where the peculiar intermingles with the profound, questioning the very essence of alteration and human existence. It is through this absurdist tapestry where each choice begets its consequence, every decision a reflection of one's ethos, that the player encounters the dark irony of the gigantesque insect that is Gregor."

    // Update the background story textarea with the content from the author's feedback
    backgroundStoryTextarea.value = feedbackContent;
  });

    submitButton.addEventListener('click', function() {
    console.log('in submit');
    var backgroundStoryText=document.getElementById('background-story').value;
    console.log(backgroundStoryText);
    // Display the background story in the textarea in the parent page
    document.getElementById('generated-background-story').value = backgroundStoryText;
    console.log("Hidden Textarea Value:", document.getElementById('generated-background-story').value); // Debugging
     // Close the modal and make the background story visible
    formGroup.classList.remove('hidden');
     $('#BackgroundStoryModal').modal('hide');
    });

});









