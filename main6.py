import os

from src.svuchatbot_features_managment import KeyWordExtractors, Definitions

kwe = KeyWordExtractors(
        source=("chatbot", "Mails-4"),
        cpu_count=os.cpu_count(),
        field_name="replay-message",
        min_weight=0.01,
        ngram="{}-Gram".format(1),
        normalize=True,
        # prefix="simple",
        reset_db=True
    )
kwe.set_pipe([
    Definitions.SPECIALWORDSEXTRACTION
            # Definitions.SIMPLETOKENIZATION,
            # Definitions.STOPWORDSREMOVING,
            # Definitions.MORPHOLOGICALTOKENIZATION,
            # Definitions.STOPWORDSREMOVING,
            # Definitions.NORMALIZATION,
            # Definitions.STOPWORDSREMOVING,
            # Definitions.BAGOFWORDSEXTRACION
        ])
kwe.work()