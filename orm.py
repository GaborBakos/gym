import numpy
import pandas

def brzycki(w, r):
    """
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on the Brzycki formula
    """
    return w * 36 / (37 - r)


def epley(w, r):
    """
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on the Epley formula
    """
    return w * (1 + r / 30)


def landers(w, r):
    """
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on the Lander's formula
    """
    return 100 * w / (101.3 - 2.67123 * r)


def lombardi(w, r):
    """
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on the Lombardi formula
    """
    return w * r ** 0.1


def mayhew(w, r):
    """
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on the Mayhew formula
    """
    return 100 * w / (52.2 + (41.9 * numpy.exp(-0.055 * r)))


def o_conner(w, r):
    """
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on the O'Conner formula
    """
    return w * (1 + (0.025 * r))


def watham(w, r):
    """
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on the Watham formula
    """
    return 100 * w / (48.8 + (53.8 * numpy.exp(-0.075 * r)))


def adjusted_bench_press(w, r):
    """
    This calculator is intended primarily for 1RM bench press calculations and
    uses a composite of the Brzycki, Epley, Wathan and Mayhew formulas adjusted
    for bench press specifics.
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on the http://maxcalculator.com/
    """
    return (0.00004 * r ** 3 - 0.0009 * r ** 2 + 0.0423 * r + 0.95856) * w


def adjusted_deadlift(w, r):
    """
    This calculator uses a formula that is optimized for calculcating your 1RM
    deadlift weight. It uses a composite of the Lombardi and O'Connor formulas and the
    National Strength and Conditioning Association (NSCA) deadlift coefficients.
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on http://maxcalculator.com/deadlift.html
    """
    return (0.00004 * r ** 3 - 0.0009 * r ** 2 + 0.0423 * r + 0.95856) * w


def adjusted_squat(w, r):
    """
    This calculator uses a formula that is optimized for calculcating your 1RM
    squat weight. It uses a composite of the Brzycki and Lander formulas and the
    National Strength and Conditioning Association (NSCA) squat coefficients.
    :param w: weight lifted
    :param r: number of reps performed
    :return: the one rep maximum based on http://maxcalculator.com/squat.html
    """
    return (0.00006 * r ** 3 - 0.0006 * r ** 2 + 0.0396 * r + 0.96094) * w


def percentage_of_orm(orm, percentages=None):
    if percentages is None:
        percentages = [1 - x for x in numpy.arange(0, 0.51, 0.05)]
    return {int(round(percentage * 100, 0)): round(percentage * orm, 2)
            for percentage in percentages}


def bisection_algorithm(func, lower_bound, upper_bound, eps=0.01):
    """
    :param func: the function of which we are trying to find the root of
    :param lower_bound:
    :param upper_bound:
    :param eps:
    :return:
    """
    def _same_sign(x, y):
        return x * y > 0

    error = numpy.inf
    num_runs = 0
    mid_point = None
    while error > eps or num_runs > 1000:
        mid_point = (lower_bound + upper_bound) / 2
        if _same_sign(func(lower_bound), func(mid_point)):
            lower_bound = mid_point
        else:
            upper_bound = mid_point
        error = numpy.abs(func(mid_point))
        num_runs += 1
    return mid_point


def avg_orm(w, r):
    return (brzycki(w, r) + epley(w, r) + landers(w, r)) / 3


def repetition_percentages_of_orm(orm, orm_calculator=None, repetitions=None):
    def f(_orm, reps, func=orm_calculator):
        return bisection_algorithm(func=lambda w: func(w, reps) - _orm,
                                   lower_bound=0,
                                   upper_bound=_orm)
    if repetitions is None:
        repetitions = list(range(1, 31))
    if orm_calculator is None:
        res1 = {reps: f(orm, reps, brzycki) for reps in repetitions}
        res2 = {reps: f(orm, reps, epley) for reps in repetitions}
        res3 = {reps: f(orm, reps, landers) for reps in repetitions}
        res = dict(pandas.DataFrame([res1, res2, res3], index=['Brzycki', 'Epley', 'Landers']).mean())
    else:
        res = {reps: f(orm, reps, orm_calculator) for reps in repetitions}

    return res


# print(percentage_of_orm(int(adjusted_bench_press(120, 5)), [1, 0.9, 0.85]))
#
# print(repetition_percentages_of_orm(int(adjusted_bench_press(120, 5)), adjusted_bench_press))
#



# // Coefficients
# nscaCoefficients = {
#   squat:    [1, 1.0650, 1.130, 1.1470, 1.164, 1.181, 1.198, 1.232, 1.232, 1.240],
#   bench:    [1, 1.0475, 1.130, 1.1575, 1.200, 1.242, 1.284, 1.326, 1.368, 1.410],
#   deadlift: [1, 1.0350, 1.080, 1.1150, 1.150, 1.180, 1.220, 1.255, 1.290, 1.325]
# }
#
# function get1RM(weight, reps, method) {
#
#   var rm1 = 0;
#
#   if ( method == "brzycki" ) {
#     rm1= weight / (1.0278 - (0.0278 * reps));
#   }
#
#   else if ( method == "epley" ) {
#     rm1= weight * ( 1 + ( reps / 30));
#   }
#
#   else if ( method == "lander" ) {
#     rm1= weight / ( 1.013 - ( 0.0267123 * reps ) );
#   }
#
#   else if ( method == "Squat" ) {
#     rm1= weight * nscaCoefficients.squat[reps-1];
#   }
#
#   else if ( method == "Bench" ) {
#     rm1= weight * nscaCoefficients.bench[reps-1];
#   }
#
#   else if ( method == "Deadlift" ) {
#     rm1= weight * nscaCoefficients.deadlift[reps-1];
#   }
#
#   return rm1;
# }
#
# function calcCoefficients(method) {
#   var coefficients = [];
#
#   var n=0;
#   while(n < 10) {
#     if ( n == 0 )
#       coefficients[n] = 1;
#     else
#       coefficients[n] = get1RM(1,n+1,method);
#     n++;
#   }
#
#   return(coefficients);
# }
#
# var percents = [100,95,90,85,80,75,70,65,60,50];
#
# var repsdata = {
#   data: {
#     replabels: ['Reps', 'Est A', 'Est B', 'Est C'],
#     percentlabels: ['Percent', 'Est A', 'Est B', 'Est C'],
#     reps: [],
#     percentages: []
#   }
# };
#
# var nsca = 'No NSCA calculation';
#
# function updateData(weight, reps, nsca) {
#   var brzycki_c = calcCoefficients("brzycki");
#   var epley_c = calcCoefficients("epley");
#   var lander_c = calcCoefficients("lander");
#   var brzycki_1rm = get1RM(weight, reps, "brzycki");
#   var epley_1rm = get1RM(weight, reps, "epley");
#   var lander_1rm = get1RM(weight, reps, "lander");
#
#   repsdata.data.reps = [];
#   repsdata.data.percentages = [];
#
#   for (i = 0; i < 10; i++) {
#     reps1=i+1;
#     reps2=(brzycki_1rm / brzycki_c[i]).toFixed(0);
#     reps3=(epley_1rm / epley_c[i]).toFixed(0);
#     reps4=(lander_1rm / lander_c[i]).toFixed(0);
#
#     perc1=percents[i].toFixed(0)+'%';
#     perc2=(brzycki_1rm * percents[i]/100).toFixed(0);
#     perc3=(epley_1rm * percents[i]/100).toFixed(0);
#     perc4=(lander_1rm * percents[i]/100).toFixed(0);
#
#     if (nsca != 'No NSCA calculation') {
#       if (nsca == 'Bench')
#         reps5=(get1RM(weight, reps, nsca) / nscaCoefficients.bench[i]).toFixed(0);
#       else if (nsca == 'Deadlift')
#         reps5=(get1RM(weight, reps, nsca) / nscaCoefficients.deadlift[i]).toFixed(0);
#       else if (nsca == 'Squat')
#         reps5=(get1RM(weight, reps, nsca) / nscaCoefficients.squat[i]).toFixed(0);
#
#       perc5=(get1RM(weight, reps, nsca) * percents[i]/100).toFixed(0);
#
#       repsdata.data.reps.push([reps1,reps2,reps3,reps4, reps5]);
#       repsdata.data.percentages.push([perc1,perc2,perc3,perc4, perc5]);
#     }
#     else {
#       repsdata.data.reps.push([reps1,reps2,reps3,reps4]);
#       repsdata.data.percentages.push([perc1,perc2,perc3,perc4]);
#     }
#   }
#
#   // Adjust labels
#   if (nsca != 'No NSCA calculation') {
#     repsdata.data.replabels[4] = nsca.toString();
#     repsdata.data.percentlabels[4] = nsca.toString();
#   }
#   else {
#     repsdata.data.replabels.splice(4);
#     repsdata.data.percentlabels.splice(4);
#   }
# }
#
# var chartdata = {
#   // A labels array that can contain any sort of values
#   labels: [10,9,8,7,6,5,4,3,2,1],
#   // Our series array that contains series objects or in this case series data arrays
#   series: []
# };
#
# var chart = null;
#
# function updateChartData() {
#
#   chartdata.series = [];
#
#   for (n = 0; n < 3; n++) {
#     var arr = [];
#     for (i=0; i < repsdata.data.reps.length; i++) {
#       arr.push(repsdata.data.reps[i][n+1]);
#     }
#     chartdata.series.push(arr.reverse());
#   }
#
# }
#
# function updateCalculations() {
#   weight = $("#weightInput").val();
#   reps = $("#repsInput").val();
#   rm1 = 0;
#
#   if ( reps < 1 || reps > 10 )
#     return;
#
#   updateData(weight, reps, nsca);
#
#   // Create the tables with templates
#   var source   = $("#reps-template").html();
#   var template = Handlebars.compile(source);
#   $("#calculationsTable").html(template(repsdata));
#
#   var source   = $("#percentages-template").html();
#   var template = Handlebars.compile(source);
#   $("#percentagesTable").html(template(repsdata));
# }
#
# function changeValue(input, delta, min, max) {
#
#   if (input == 'weight') {
#     val = $("#weightInput").val();
#   } else if (input == 'reps') {
#     val = $("#repsInput").val();
#   }
#
#   newVal = parseInt(val) + delta;
#
#   if (!isNaN(newVal) && newVal >= min && newVal <= max)
#     val = newVal;
#   else
#     val = val;
#
#   if (input == 'weight') {
#     $("#weightInput").val(val);
#   } else {
#     $("#repsInput").val(val);
#   }
#   updateCalculations();
# }
#
# function showOverlay() {
#   document.getElementById("overlay").style.display = "block";
#   updateChartData();
#   chart = new Chartist.Line('.ct-chart', chartdata);
# }
#
# function hideOverlay() {
#   document.getElementById("overlay").style.display = "none";
# }
#
# // Prepare scripts
#
# $(document).ready(function(){
#
#   nsca = $('#nsca-selector').val();
#
#   // On document load
#   updateCalculations();
#
#   // On input value change
#
#   $('#repsInput').on('input',function(e){ updateCalculations(); });
#
#   $('#weightInput').on('input',function(e){ updateCalculations(); });
#
#   $('#nsca-selector').change(function() {
#     nsca=$(this).val();
#     updateCalculations();
#   });
#
#   // Button click handlers
#
#   $('#increase-weight-button').on('click',function(e){ changeValue('weight', 5, 1, 9999); });
#   $('#decrease-weight-button').on('click',function(e){ changeValue('weight', -5, 1, 9999); });
#   $('#increase-reps-button').on('click',function(e){ changeValue('reps', 1, 1, 10); });
#   $('#decrease-reps-button').on('click',function(e){ changeValue('reps', -1, 1, 10); });
#
#   // Add email
#   $('span#email-address').text('htapio @ outlook.com');
#
# });
