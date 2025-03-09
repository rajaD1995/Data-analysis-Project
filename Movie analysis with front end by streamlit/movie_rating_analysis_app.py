import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Load titanic dataset
@st.cache_data
def load_data():
    movie = pd.read_csv(r'C:\Users\USER\Documents\Python\Nareshit data analysis\Data analysis\MOVIE RATINGS _ ADVANCE VISUALIZATION _ EDA 1\Movie analysis with front end by streamlit\Movie-Rating.csv')
    movie.columns=['Film', 'Genre', 'CriticsRating', 'AudienceRatings', 'BudgetMillion','Year']
    for col in movie.columns:
        if movie[col].dtype == 'object':
            movie[col] = movie[col].astype('category')
    movie['Year']=movie['Year'].astype('category')
    return movie

movie = load_data()

st.image("movie_logo.webp")
st.title("Data analysis of movies by Raja Debnath")
st.header("This is an EDA on the movies Dataset")
st.write('First few rows of the dataset: ')
st.dataframe(movie.head())

#check_for_empty_cell
st.subheader('Missing Values')
missing_data = movie.isnull().sum()
st.write(missing_data)

# EDA Section
st.subheader('Statistical Summary of the Data')
st.write(movie.describe().T)
# st.write(movie.dtypes)  # .info() is not working.

st.info("Visualization")
#visualization
#Graph 1
# Subheader
st.subheader('Distribution of Critics Rating & Audience Ratings')
# Plot the jointplot
vis1 = sns.jointplot(
    data=movie,
    x='CriticsRating',      # Make sure column name is exactly correct
    y='AudienceRatings',
    kind="reg",
    height=4,
    ratio=4
)
# Set the figure size manually (optional)
vis1.figure.set_size_inches(5, 4)
# Add a title to the figure
plt.suptitle("Critics Rating vs Audience Rating", fontsize=10)
plt.tight_layout()
# Render the plot in Streamlit
st.pyplot(vis1.figure)

#Graph 2
# Subheader
st.subheader('Distribution of Audience Ratings')
vis2 = sns.displot(movie.AudienceRatings)
plt.gcf().set_size_inches(3, 2)
st.pyplot(vis2.figure)

#Graph 3
# Subheader
st.subheader('Stacked Distribution')
plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
plt.hist(
    [movie[movie.Genre==gen].AudienceRatings for gen in movie.Genre.cat.categories],
    bins=20,
    label=movie.Genre.cat.categories,
    alpha=1,   #make color dull or bright
    stacked=True,
)
# plt.gcf().set_size_inches(10, 6)
# Add labels and title
plt.xlabel('Audience Rating')
plt.ylabel('Frequency')
plt.title('Stacked Distribution of Audience Ratings by Genre')
plt.subplot(1, 2, 2)
# Plot stacked histogram
plt.hist(
    [movie[movie.Genre==gen].BudgetMillion for gen in movie.Genre.cat.categories],
    bins=20,
    label=movie.Genre.cat.categories,
    alpha=1,   #make color dull or bright
    stacked=True
)
# plt.gcf().set_size_inches(7, 5)
# Add labels and title
plt.xlabel('Budget in Million ($)')
plt.ylabel('Frequency')
plt.title('Stacked Distribution of Budget by Genre')
# Add legend
plt.legend()
plt.show()
# ✅ The correct way to show the figure
st.pyplot(plt.gcf())


#Graph 4
if st.checkbox('Boxplot for Genre wise Critics Rating & Audience Ratings'):
    # Subheader
    st.subheader('Genre wise Critics Rating & Audience Ratings')
    color_dict = {
        'Action': 'skyblue',
        'Drama': 'lightcoral',
        'Comedy': 'lightgreen',
        'Thriller': 'orange',
        'Horror': 'purple',
        'Romance': 'red',
        'Adventure': 'gold'
    }
    fig, ax = plt.subplots(1,2,figsize=(14,6))
    sns.boxplot(data=movie, x='Genre',y='CriticsRating', palette=color_dict, ax = ax[0])
    #Modifying the shape & size of x,y label and title & ticks.
    ax[0].set_xlabel('Genre', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
    ax[0].set_ylabel('Critics Rating', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
    ax[0].set_xticklabels(ax[0].get_xticklabels(), fontweight='bold', fontsize=10)
    ax[0].set_yticklabels(ax[0].get_yticklabels(),fontweight='bold', fontsize=10)

    sns.boxplot(data=movie, x='Genre',y='AudienceRatings',palette=color_dict, ax = ax[1])
    #Modifying the shape & size of x,y label and title & ticks.
    ax[1].set_xlabel('Genre', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
    ax[1].set_ylabel('Audience Rating', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
    ax[1].set_xticklabels(ax[1].get_xticklabels(),fontweight='bold', fontsize=10)
    ax[1].set_yticklabels(ax[1].get_yticklabels(),fontweight='bold', fontsize=10)
    plt.show()
    st.pyplot(fig)


#Graph 5
if st.checkbox('FacetGrid for Audience Ratings vs Budget split by Genre and Year'):
    # Subheader
    st.subheader('Audience Ratings vs Budget split by Genre and Year')
    # Plot FacetGrid to understand Genre vs Year vs Audience Ratings
    g = sns.FacetGrid(data=movie, row='Genre', col='Year', hue='Genre', height=2, aspect=1.3)
    g.map(sns.scatterplot, 'AudienceRatings', 'BudgetMillion', alpha=0.7)

    # Adjust plot
    # g.add_legend()
    plt.subplots_adjust(top=0.9)
    # g.fig.suptitle('Audience Ratings vs Budget split by Genre and Year')
    plt.show()
    st.pyplot(g.figure)

#Graph 6
if st.checkbox('Year wise boxplot of Audience rating'):
    # Subheader
    st.subheader('Year wise Audience Rating for Genre Films')

    # ✅ Capture the figure object
    fig = plt.figure(figsize=(20,16))

    # ✅ Loop through each genre and create boxplots
    for i, gen in enumerate(movie.Genre.cat.categories):
        ax = plt.subplot(4,2,i+1)
        sns.boxplot(data=movie[movie.Genre==gen],  x='Year',y='AudienceRatings', ax=ax)

        # ✅ Add Titles and Labels. #Modifying the shape & size of x,y label and title & ticks.
        ax.set_title(f'Year wise Audience rating for {gen} film', fontweight='bold', fontsize=20)
        ax.set_xlabel('Year', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
        ax.set_ylabel('Audience Rating', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
        ax.set_xticklabels(ax.get_xticklabels(),fontweight='bold', fontsize=20)
        ax.set_yticklabels(ax.get_yticklabels(),fontweight='bold', fontsize=20)

        # ✅ Customize the Tick Labels
        ax.set_xticklabels(ax.get_xticklabels(), fontweight='bold', fontsize=20, rotation=45)
        ax.set_yticklabels(ax.get_yticklabels(), fontweight='bold', fontsize=10)

    # ✅ Adjust Layout
    plt.tight_layout()

    # ✅ Show the figure in Streamlit
    st.pyplot(fig)



#Graph 7
# Subheader
st.subheader('Average rating by Genre')
# Group data by Genre and calculate mean ratings
audience_mean = movie.groupby('Genre')['AudienceRatings'].mean().sort_values(ascending=False).to_frame()  #.to_frame()--- series to dataframe.
critics_mean = movie.groupby('Genre')['CriticsRating'].mean().sort_values(ascending=False).to_frame()
# Define colors for the heatmap
colors = ['#F93822','#FDD20E']
# Plot two side-by-side heatmaps
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 5)) # the gnre names comes vertically or horizontally depends on figsize

# Heatmap 1: Audience Ratings by Genre
plt.subplot(1, 2, 1)
sns.heatmap(audience_mean, annot=True, cmap=colors, linewidths=0.4, linecolor='black', cbar=False, fmt='.2f')
plt.title('Average Audience Rating by Genre')

# Heatmap 2: Critics Ratings by Genre
plt.subplot(1, 2, 2)
sns.heatmap(critics_mean, annot=True, cmap=colors, linewidths=0.4, linecolor='black', cbar=False, fmt='.2f')
plt.title('Average Critics Rating by Genre')

# Adjust layout
fig.tight_layout(pad=2)
st.pyplot(fig)


#Graph 8
#Dashboard
# Subheader
st.subheader('Dashboard')
sns.set_style('ticks')
f, ax = plt.subplots(2, 2, figsize=(15, 15))

# Plot 1: Without Shade
k1 = sns.kdeplot(movie, y='AudienceRatings', x='BudgetMillion', cmap='cool', ax=ax[0, 0])

# Plot 2: With Shade and Different Colormap
k1b = sns.kdeplot(movie, y='AudienceRatings', x='BudgetMillion', cmap='magma', ax=ax[0, 0],
                  shade=True, shade_lowest=True)
#Modifying the shape & size of x,y label and title & ticks.
ax[0,0].set_title('Audience Ratings vs Budget in Million', fontsize=20)
ax[0,0].set_xlabel('Budget in Million', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
ax[0,0].set_ylabel('Audience Rating', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
ax[0,0].set_xticklabels(ax[0,0].get_xticklabels(),fontweight='bold', fontsize=20)
ax[0,0].set_yticklabels(ax[0,0].get_yticklabels(),fontweight='bold', fontsize=20)
k1.set(xlim=(-50,250))

# Plot 1: Without Shade
k2 = sns.kdeplot(movie, y='CriticsRating', x='BudgetMillion', cmap='magma',thresh=0.05 , ax=ax[0, 1],
                  shade=True, shade_lowest=True)
# Plot 2: With Shade and Different Colormap
k2b = sns.kdeplot(movie, y='CriticsRating', x='BudgetMillion', cmap='Blues', ax=ax[0, 1])
ax[0, 1].set_facecolor('lightblue')
#Modifying the shape & size of x,y label and title & ticks.
ax[0,1].set_title('Critics Ratings vs Budget in Million', fontsize=20)
ax[0,1].set_xlabel('Budget in Million', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
ax[0,1].set_ylabel('Critics Rating', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
ax[0,1].set_xticklabels(ax[0,1].get_xticklabels(),fontweight='bold', fontsize=20)
ax[0,1].set_yticklabels(ax[0,1].get_yticklabels(),fontweight='bold', fontsize=20)
k2.set(xlim=(-50,250))

k3= sns.violinplot(movie[movie.Genre == 'Thriller'], x='Year', y='AudienceRatings', ax = ax[1,0])
#Modifying the shape & size of x,y label and title & ticks.
ax[1,0].set_title('Year wise Audience Ratings for Thriller', fontsize=20)
ax[1,0].set_xlabel('Year', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
ax[1,0].set_ylabel('Audience Rating', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
ax[1,0].set_xticklabels(ax[1,0].get_xticklabels(),fontweight='bold', fontsize=20)
ax[1,0].set_yticklabels(ax[1,0].get_yticklabels(),fontweight='bold', fontsize=20)

k4 = sns.kdeplot(movie, x= 'CriticsRating',y='AudienceRatings', \
                 shade = True,shade_lowest=False,cmap='Blues_r', \
                 ax=ax[1,1])
k4b = sns.kdeplot(movie, x= 'CriticsRating',y='AudienceRatings', \
                  cmap='gist_gray_r',ax = ax[1,1])
#Modifying the shape & size of x,y label and title & ticks.
ax[1,1].set_title('Critics Rating vs Audience Ratings', fontsize=20)
ax[1,1].set_xlabel('Critics Rating', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
ax[1,1].set_ylabel('Audience Rating', fontweight='bold', fontsize=20, fontfamily='serif', color='black')
ax[1,1].set_xticklabels(ax[1,1].get_xticklabels(),fontweight='bold', fontsize=20)
ax[1,1].set_yticklabels(ax[1,1].get_yticklabels(),fontweight='bold', fontsize=20)

st.pyplot(f)


# Conclusion Section
st.subheader('Key Insights')
insights = """
- Thriller, Drama, Adventure are the top rating movies.
- Audiance rating are more generous than critic rating.
- Audiance rating & critic rating have liner relation.
- Movies having higher Audiance rating, are likely to be watched by audiance.
- Horror movies have bad impact on audiance.
"""
st.write(insights)