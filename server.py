from flask import Flask, render_template, request
import seaborn as sns
import plotly
import plotly.graph_objs as go
import json 

app = Flask(__name__)

#####################
# FUNCTION FOR PLOT #
#####################

# Histogram dan Boxplot func
def category_plot(cat_plot = 'histoplot', cat_x = 'sex', cat_y = 'total_bill', estimator = 'count', hue = 'smoker'):
    
    dfTips = sns.load_dataset('tips')

    if cat_plot == 'histoplot':
        data = []

        for val in dfTips[hue].unique(): # [No, Yes]
            hist = go.Histogram(
                
                    x = dfTips[dfTips[hue] == val][cat_x],
                    y = dfTips[dfTips[hue] == val][cat_y],
                    histfunc = 'count',
                    name = val

                    )
            
            data.append(hist)

        title = 'HISTOGRAM'
    else:
        data = []

        for val in dfTips[hue].unique(): # [No, Yes]
            hist = go.Box(
                
                    x = dfTips[dfTips[hue] == val][cat_x],
                    y = dfTips[dfTips[hue] == val][cat_y],
                    name = val

                    )
            
            data.append(hist)

        title = "BOXPLOT"

    layout = go.Layout(

        title = title,

        title_x = 0.5,

        xaxis = dict(title = cat_x),

        yaxis = dict(title = cat_y),

        boxmode = 'group'

    )

    final = {'data' : data, 'layout' : layout}

    graphJSON = json.dumps(final, cls = plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# Scatter Plot func
def scatter_plot(cat_x, cat_y):
    # sumber data
    dfTips = sns.load_dataset('tips')

    # Masukan data
    data_src = [
        
        go.Scatter(
        
            x = dfTips[cat_x],
            
            y = dfTips[cat_y],
            
            mode = 'markers'
            
        )
        
    ]

    # Pembuatan layout
    layout_src = go.Layout(

        title = 'SCATTER PLOT',
        
        title_x = 0.5,
        
        xaxis = dict(title = cat_x),
        
        yaxis = dict(title = cat_y)
        
    )

    # Gabungkan antara data dan layout dalam satu variabel
    # key 'data' dan 'layout' harus ada
    final = {'data' : data_src, 'layout' : layout_src}

    graphJSON = json.dumps(final, cls = plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# Pie plot func
def pie_plot(cat):
    
    dfTips = sns.load_dataset('tips')
    result = dfTips[cat].value_counts()
    
    labels = []
    values = []

    for i in result.iteritems():
        labels.append(i[0])
        values.append(i[1])
        
    data_src = [
        
        go.Pie(
        
            labels = labels,
            
            values = values,
            
        )
        
    ]

    layout_src = go.Layout(

        title = 'PIE',
        
        title_x = 0.5,
        
    )

    final = {'data' : data_src, 'layout' : layout_src}

    graphJSON = json.dumps(final, cls = plotly.utils.PlotlyJSONEncoder)

    return graphJSON

######################
# FUNCTION FOR ROUTE #
######################

@app.route('/')
def index():
    plot = category_plot()

    return render_template(
        'category.html', 
        plot = plot, 
        focus_plot = 'histoplot', 
        focus_x = 'sex', 
        focus_y = 'total_bill', 
        focus_estimator = 'count'
    )

@app.route('/cat_fn')
def cat_fn():
    # Request untuk ambil data dari form
    cat_plot = request.args.get('cat_plot')
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    estimator = request.args.get('estimator')
    hue = request.args.get('hue')

    if cat_plot == None and cat_x == None and cat_y == None and estimator == None and hue == None:
        cat_plot = 'histoplot'
        cat_x = 'sex'
        cat_y = 'total_bill'
        estimator = 'count'
        hue = 'smoker'

    if estimator == None:
        estimator = 'count'

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)

    # List dropdown
    drop_plot_src = [('histoplot', 'Histogram'), ('boxplot', 'Boxplot')]
    drop_x_src = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]
    drop_y_src = [('total_bill', 'Total Bill'), ('tip', 'Tip'), ('size', 'size')]
    drop_est_src = [('count', 'Count'), ('sum', 'Sum'), ('avg', 'Average'), ('min', 'Minimum'), ('max', 'Maximum')]

    return render_template(
        'category.html', 
        plot = plot, 
        focus_plot = cat_plot, 
        focus_x = cat_x, 
        focus_y = cat_y, 
        focus_estimator = estimator,
        focus_hue = hue,
        drop_plot = drop_plot_src,
        drop_x = drop_x_src,
        drop_y = drop_y_src,
        drop_est = drop_est_src,
        drop_hue = drop_x_src

    )

@app.route('/scat_fn')
def scat_fn():

    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')

    if cat_x == None and cat_y == None:
        cat_x = 'total_bill'
        cat_y = 'tip'

    plot = scatter_plot(cat_x, cat_y)

    return render_template('scatter.html', plot = plot, focus_x = cat_x, focus_y = cat_y)

@app.route('/pie_fn')
def pie_fn():

    cat = request.args.get('cat')

    if cat == None:
        cat = 'sex'

    plot = pie_plot(cat)

    return render_template('pie.html', plot = plot, focus_cat = cat)

if __name__ == '__main__':
    app.run(debug = True)