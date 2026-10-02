"""LinkedIn complete prompts; merge the identical Meesho server assignment."""


def extend(add, merge):
    merge('meesho-server-index','LinkedIn',[
        'WhatsApp Image 2024-08-01 at 12.20.49_78e3eabb.jpg',
        'WhatsApp Image 2024-08-01 at 12.21.10_62dfe1cd.jpg',
        'WhatsApp Image 2024-08-01 at 12.21.39_46a36c33.jpg',
        'WhatsApp Image 2024-08-01 at 12.22.37_83cc2ba1.jpg'])
    add('linkedin-positive-meetings','LinkedIn','Order meetings to keep a positive effectiveness index',
        'A manager begins with effectiveness index zero. Each meeting changes it by the given signed effectiveness value. Rearrange the meetings to maximise how many can be held while the running index stays strictly greater than zero after every held meeting. Return that maximum number.',None,
        'Sort effectiveness in decreasing order and accumulate. Count meetings until the next cumulative sum is zero or negative. The largest k values have the greatest possible sum of any k meetings, so no other order can make a length-k prefix positive if the descending prefix is nonpositive. Descending order also keeps earlier sums as large as possible. Once a descending prefix fails, its latest contribution is nonpositive and all later contributions are no larger, so recovery cannot occur. Strict positivity means a zero sum does not count. O(n log n) time and O(n) space for a sorted copy; use a wide running sum.',
        section='dsa',topic='greedy',type='coding',sources=['IMG-20240801-WA0025.jpg','IMG-20240801-WA0027.jpg'],
        function_signature='maxMeetings(effectiveness)',constraints='1 ≤ n ≤ 10⁵; −10⁹ ≤ effectiveness[i] ≤ 10⁹.',
        examples=[{'input':'effectiveness = [1,-20,3,-2]','output':'3'}, {'input':'effectiveness = [-3,0,2,1]','output':'3'}])
    add('linkedin-festival-cost','LinkedIn','Minimum population-weighted Manhattan travel cost',
        'City i is at integer coordinates (x[i],y[i]) and has numPeople[i] residents. A festival can be located at any integer point (a,b). Every resident attends and pays |x[i]−a|+|y[i]−b|. Return the minimum total travel cost over all locations.',None,
        'The x and y terms separate. For each coordinate axis, sort cities by that coordinate, accumulate their populations and select the first coordinate where twice the cumulative population is at least the total. This is a weighted median. Place the festival at the independently chosen x and y weighted medians and sum each city’s population times its Manhattan distance. Moving across a coordinate changes the slope by twice the population there; a median balances weight on both sides. Do not use an unweighted median or arithmetic mean. O(n log n) time and O(n) space. When the total population is split equally, an interval of integer coordinates can be optimal; any weighted median endpoint suffices.',
        section='dsa',topic='math',type='coding',sources=[f'IMG-20240801-WA00{i}.jpg' for i in (26,28,29,30)],
        function_signature='minimizeCost(numPeople, x, y)',constraints='1 ≤ n ≤ 10³; 1 ≤ x[i],y[i] ≤ 10⁴; 1 ≤ numPeople[i] ≤ 50.',
        examples=[{'input':'numPeople = [1,2]\nx = [1,3]\ny = [1,3]','output':'4','explanation':'Hold it at (3,3).'}, {'input':'numPeople = [1,1]\nx = [1,3]\ny = [1,1]','output':'2','explanation':'Any location (a,1) with a in {1,2,3} is optimal.'}],
        notes='The second source example lists optimal coordinates in reversed order; the cleaned example follows the stated x/y arrays and Manhattan formula.')
