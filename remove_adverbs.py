import re
import sys
import pyperclip

# List of predefined adverbs
ADVERB_REGEX = r'\b(always|constantly|continually|frequently|never|occasionally|periodically|rarely|regularly|seldom|sometimes|absolutely|almost|barely|completely|deeply|enormously|exceedingly|highly|incredibly|merely|moderately|partially|perfectly|purely|quite|really|simply|somewhat|substantially|totally|utterly|very|angrily|anxiously|awkwardly|beautifully|bitterly|boldly|calmly|carefully|cheerfully|clearly|coolly|correctly|deliberately|eagerly|elegantly|energetically|enthusiastically|foolishly|gracefully|happily|honestly|lazily|loudly|quickly|quietly|rapidly|smoothly|steadily|strangely|vividly|immediately|instantly|later|meanwhile|now|previously|recently|soon|apparently|arguably|basically|certainly|doubtfully|evidently|finally|indeed|likely|maybe|only|possibly|presumably|probably|ultimately|virtually|abnormally|abroad|absentmindedly|accidentally|actively|acutely|admiringly|affectionately|affirmatively|agreeably|already|amazingly|annoyingly|annually|anyhow|anyplace|anyway|anywhere|appreciably|appropriately|arrogantly|assuredly|astonishingly|awfully|badly|bashfully|begrudgingly|believably|bewilderedly|bewilderingly|bleakly|blindly|blissfully|boastfully|boyishly|bravely|briefly|brightly|brilliantly|briskly|brutally|busily|candidly|carelessly|casually|cautiously|charmingly|chiefly|childishly|cleanly|cleverly|closely|cloudily|clumsily|coaxingly|coincidentally|coldly|colorfully|comfortably|commonly|compactly|compassionately|confusedly|considerably|considerately|consistently|continuously|courageously|covertly|cowardly|crazily|crossly|cruelly|cunningly|curiously|customarily|cutely|daily|daintily|dangerously|daringly|darkly|dastardly|dearly|decently|defiantly|deftly|delicately|delightfully|densely|diagonally|differently|diligently|dimly|directly|disorderly|divisively|docilely|dopily|dramatically|dreamily|early|earnestly|easily|efficiently|effortlessly|elaborately|eloquently|elsewhere|emotionally|endlessly|enjoyably|enough|entirely|equally|especially|essentially|eternally|ethically|even|evenly|evermore|every|everywhere|evocatively|exactly|excitedly|explicitly|expressly|extensively|externally|extra|extraordinarily|faithfully|famously|far|fashionably|fast|fatally|favorably|ferociously|fervently|fiercely|fiery|financially|finitely|fluently|fondly|forever|fortunately|frankly|frantically|freely|frenetically|fully|furiously|generally|generously|gently|girlishly|gladly|gleefully|graciously|gradually|gratefully|greatly|greedily|grimly|grudgingly|habitually|half-heartedly|handily|handsomely|haphazardly|harmoniously|harshly|hatefully|hauntingly|healthily|heartily|heavily|helpfully|hopelessly|horizontally|hourly|hugely|humorously|hungrily|hurriedly|hysterically|icily|identifiably|idiotically|imaginatively|immeasurably|immensely|impatiently|impressively|inappropriately|incessantly|incorrectly|independently|indoors|indubitably|inevitably|infinitely|informally|infrequently|innocently|inquisitively|intelligently|intensely|intently|intermittently|internally|invariably|invisibly|inwardly|ironically|irrefutably|irritably|jaggedly|jauntily|jealously|jovially|joyfully|joylessly|joyously|jubilantly|judgmentally|justly|keenly|kiddingly|kindheartedly|kindly|knavishly|knottily|knowingly|knowledgeably|kookily|lastly|late|lately|lightly|limply|lithely|lively|loftily|longingly|loosely|lovingly|loyally|luckily|luxuriously|madly|magically|mainly|majestically|markedly|materially|meaningfully|meanly|meantime|measurably|mechanically|medically|menacingly|merrily|methodically|mightily|miserably|mockingly|monthly|morally|mortally|mysteriously|nastily|naturally|naughtily|nearby|nearly|neatly|needily|negatively|nervously|nicely|nightly|noisily|normally|nosily|nowadays|numbly|obediently|obligingly|obnoxiously|oddly|offensively|officially|often|ominously|once|openly|optimistically|orderly|outdoors|outrageously|outwardly|outwards|overconfidently|overseas|painfully|painlessly|paradoxically|particularly|passionately|patiently|perpetually|persistently|personally|persuasively|physically|plainly|playfully|poetically|poignantly|politely|poorly|positively|potentially|powerfully|presently|prettily|primly|principally|properly|proudly|punctually|puzzlingly|quaintly|queasily|questionably|questioningly|quicker|quirkily|quizzically|randomly|readily|reasonably|reassuringly|recklessly|reliably|reluctantly|repeatedly|reponsibly|reproachfully|resentfully|respectably|restfully|richly|ridiculously|righteously|rightfully|rightly|rigidly|roughly|routinely|rudely|ruthlessly|sadly|safely|scarcely|scarily|scientifically|searchingly|secretively|securely|sedately|seemingly|selfishly|selflessly|separately|seriously|shakily|shamelessly|sharply|sheepishly|shoddily|shortly|shrilly|shyly|silently|silicitiously|sincerely|singularly|skillfully|sleepily|slightly|slowly|slyly|softly|solemnly|solidly|somehow|somewhere|spasmodically|specially|specifically|spectacularly|speedily|spiritually|splendidly|sporadically|startlingly|stealthily|sternly|still|strenuously|stressfully|strictly|structurally|studiously|stupidly|stylishly|subtly|successfully|suddenly|sufficiently|suitably|superficially|supremely|surely|suspiciously|sweetly|swiftly|sympathetically|systematically|temporarily|tenderly|tensely|tepidly|terribly|thankfully|thoroughly|thoughtfully|tightly|today|together|tomorrow|touchingly|tremendously|truly|truthfully|twice|unabashedly|unanimously|unbearably|unbelievably|unemotionally|unethically|unexpectedly|unfailingly|unfavorably|unfortunately|uniformly|unilaterally|unimpressively|universally|unkindly|unnaturally|unnecessarily|unquestionably|unselfishly|unskillfully|unwillingly|upbeat|upliftingly|upright|upside-down|upward|upwardly|urgently|usefully|uselessly|usually|vacantly|vaguely|vainly|valiantly|vastly|verbally|vertically|viciously|victoriously|vigilantly|vigorously|violently|visibly|visually|vivaciously|voluntarily|warmly|weakly|wearily|weekly|wetly|whole-heartedly|wholly|why|wickedly|widely|wiggly|wildly|willfully|willingly|wisely|woefully|wonderfully|worriedly|worthily|wrongly|yearly|yearningly|yesterday|yet|youthfully|zanily|zealously|zestfully|zestily)\b'

def remove_adverbs(text: str) -> str:
    """Removes adverbs from the given text."""
    return re.sub(ADVERB_REGEX, '', text, flags=re.IGNORECASE)

def main():
    """Reads input from stdin, processes it, and prints cleaned text."""
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip()
        cleaned_text = remove_adverbs(text)
        print(cleaned_text)
    else:
        text = pyperclip.paste()
        cleaned_text = remove_adverbs(text)
        pyperclip.copy(cleaned_text)
        print("Processed text copied to clipboard!")

if __name__ == "__main__":
    main()